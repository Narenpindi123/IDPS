# 🛡️ Intrusion Detection System (IDS) – SYN Flood Detection

A Python-based IDS that monitors real-time network traffic to detect SYN-flood attacks.  
It logs events, sends email alerts, blocks attacker IPs with `iptables`, and displays everything on a Flask dashboard.

---

## 🚀 Features
- **SYN Flood Detection** using **Scapy**  
- **Flask Dashboard** for live attack logs  
- **Email Alerts** when an attack is detected  
- **Automatic IP Blocking** via `iptables`  
- **JSON Log Storage** (`intrusion_log.json`)  
- **Trusted IP Whitelist** (e.g. `127.0.0.1`)  

---

## 🧠 How It Works
1. **Capture**: Scapy listens for TCP SYN packets on your chosen interface.  
2. **Detect**: If one IP sends more than _N_ SYNs in a short time:  
   - Log the event (timestamp, source IP, destination port)  
   - Send an email alert  
   - Block the IP with `iptables`  
3. **Display**: Flask serves a web dashboard at `http://127.0.0.1:5000` showing all events and offering JSON download.

---

## 📁 Project Structure
IDS/
├── ids_main.py # Main detection & web-server script
├── config.ini # Email & threshold settings
├── templates/
│ └── dashboard.html # Flask dashboard template
└── static/
└── intrusion_log.json # Logged attack events

---

## ⚙️ Installation & Setup

1. **Install dependencies**  
   ```bash
   pip install flask scapy
2. Create config.ini in the project root:
[EMAIL]
sender   = your_email@gmail.com
password = your_app_password
receiver = your_email@gmail.com

[DETECTION]
syn_flood_threshold = 10
alert_rate_limit    = 60
block_threshold     = 20
3. Run the IDS
sudo python3 ids_main.py
4. Access the dashboard
Open in your browser: http://127.0.0.1:5000

🧪 Simulate a SYN Flood
On a second machine (same network), run:
sudo hping3 -S -p 5000 -a 192.168.1.99 --flood 10.0.2.15
-S sends SYN packets

-p 5000 targets the Flask port

-a spoofs the attacker IP

10.0.2.15 is your IDS host
Cleanup & Reset
Stop attack:

sudo pkill hping3
Clear logs:

sudo rm static/intrusion_log.json
Flush firewall rules:

sudo iptables -F
