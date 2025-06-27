import threading
import json
import os
import time
from scapy.all import sniff, IP, TCP
import smtplib
from email.mime.text import MIMEText
import configparser
from flask import Flask, render_template

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

SENDER_EMAIL = config['email']['sender']
RECEIVER_EMAIL = config['email']['receiver']
SENDER_PASSWORD = config['email']['password']
SYN_FLOOD_THRESHOLD = int(config['detection']['syn_flood_threshold'])
ALERT_RATE_LIMIT = int(config['detection']['alert_rate_limit'])
BLOCK_THRESHOLD = int(config['detection']['block_threshold'])

# Log file setup
LOG_FILE = "static/intrusion_log.json"
if not os.path.exists("static"):
    os.mkdir("static")
if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    try:
        with open(LOG_FILE) as f:
            logs = json.load(f)
    except Exception:
        logs = []
    return render_template("index.html", logs=logs)

# Trackers
syn_flood_tracker = {}
last_email_sent = {}
blocked_ips = set()

# Logging function
def log_intrusion(activity, packet):
    log_entry = {
        "activity": activity,
        "source_ip": packet[IP].src,
        "destination_port": packet[TCP].dport,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open(LOG_FILE, "r+") as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=2)
    except Exception:
        pass
    # Minimal terminal output to avoid flood
    print(f"Logged: {log_entry['activity']} at {log_entry['timestamp']}")

# Send email with rate limiting
def send_email_alert(activity, packet):
    src_ip = packet[IP].src
    now = time.time()

    if src_ip in last_email_sent and now - last_email_sent[src_ip] < ALERT_RATE_LIMIT:
        return
    last_email_sent[src_ip] = now

    try:
        msg = MIMEText(f"Alert: {activity} from {src_ip}")
        msg["Subject"] = "IDS Alert"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"📧 Email alert sent for {src_ip}")
    except Exception as e:
        print(f"Email failed: {e}")

# Block IP only once
def block_ip(ip):
    if ip not in blocked_ips:
        os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
        blocked_ips.add(ip)
        print(f"⛔ Blocked IP: {ip}")

# Intrusion detection logic
def detect_intrusion(packet):
    if packet.haslayer(TCP) and packet.haslayer(IP):
        src_ip = packet[IP].src
        if packet[TCP].flags == "S":
            syn_flood_tracker[src_ip] = syn_flood_tracker.get(src_ip, 0) + 1

            # Add a minimal delay to reduce excessive alerts
            if time.time() - last_email_sent.get(src_ip, 0) < 10:
                return

            if syn_flood_tracker[src_ip] >= SYN_FLOOD_THRESHOLD:
                activity = f"SYN flood from {src_ip}"
                log_intrusion(activity, packet)
                send_email_alert(activity, packet)
                if syn_flood_tracker[src_ip] >= BLOCK_THRESHOLD:
                    block_ip(src_ip)

# Start packet sniffing (on loopback interface)
def start_sniffing():
    print("✅ IDS is monitoring traffic on interface: lo")
    sniff(prn=detect_intrusion, iface="lo", store=0)

# Launch IDS + Web
if __name__ == "__main__":
    threading.Thread(target=start_sniffing).start()
    app.run(host="0.0.0.0", port=5000)
