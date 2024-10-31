import threading
import logging
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

# Configurations from config.ini
SENDER_EMAIL = config['email']['sender']
RECEIVER_EMAIL = config['email']['receiver']
SENDER_PASSWORD = config['email']['password']
SYN_FLOOD_THRESHOLD = int(config['detection']['syn_flood_threshold'])
ALERT_RATE_LIMIT = int(config['detection']['alert_rate_limit'])
BLOCK_THRESHOLD = int(config['detection']['block_threshold'])

# Initialize JSON log file with an empty array if it doesn't exist or is empty
if not os.path.exists("intrusion_log.json") or os.stat("intrusion_log.json").st_size == 0:
    with open("intrusion_log.json", "w") as log_file:
        json.dump([], log_file)  # Write an empty list to make it valid JSON

# Set up Flask app for web dashboard
app = Flask(__name__)

@app.route("/")
def home():
    logs = []
    try:
        with open("intrusion_log.json") as log_file:
            logs = json.load(log_file)  # Load as a JSON array
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading log file: {e}")
    return render_template("index.html", logs=logs)

def log_intrusion(activity, packet):
    """Log detected intrusion activity in JSON format."""
    log_entry = {
        "activity": activity,
        "source_ip": packet[IP].src,
        "destination_port": packet[TCP].dport,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    # Append the log entry to the JSON array in the file
    try:
        with open("intrusion_log.json", "r+") as log_file:
            logs = json.load(log_file)
            logs.append(log_entry)
            log_file.seek(0)
            json.dump(logs, log_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error writing to log file: {e}")
    print(log_entry)

def send_email_alert(activity, packet):
    """Send an email alert about detected intrusion activity with rate limiting."""
    src_ip = packet[IP].src
    current_time = time.time()

    if src_ip in last_email_sent and current_time - last_email_sent[src_ip] < ALERT_RATE_LIMIT:
        return  # Skip sending email to avoid spamming

    last_email_sent[src_ip] = current_time  # Update the last sent time

    try:
        msg = MIMEText(f"Alert: {activity} detected from {src_ip}")
        msg["Subject"] = "Intrusion Detection Alert"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email alert sent.")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

def block_ip(ip):
    """Block an IP address using iptables."""
    os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
    print(f"Blocked IP: {ip}")

# Dictionary for tracking IPs to detect SYN flood and apply rate limiting
syn_flood_tracker = {}
last_email_sent = {}

def detect_intrusion(packet):
    """Detect suspicious network activity and take appropriate action."""
    if packet.haslayer(TCP):
        src_ip = packet[IP].src
        if packet[TCP].flags == "S":  # SYN flag set
            syn_flood_tracker[src_ip] = syn_flood_tracker.get(src_ip, 0) + 1

            # Check for SYN flood threshold
            if syn_flood_tracker[src_ip] >= SYN_FLOOD_THRESHOLD:
                activity = f"SYN flood detected from {src_ip}"
                log_intrusion(activity, packet)
                send_email_alert(activity, packet)

                # Block IP if it exceeds the block threshold
                if syn_flood_tracker[src_ip] >= BLOCK_THRESHOLD:
                    block_ip(src_ip)

def start_sniffing():
    """Start packet sniffing in a separate thread and analyze each packet."""
    print("Starting Intrusion Detection System...")
    sniff(prn=detect_intrusion, count=0)

if __name__ == "__main__":
    # Run IDS in a separate thread
    threading.Thread(target=start_sniffing).start()

    # Run the Flask app for the dashboard
    app.run(host="0.0.0.0", port=5000)
