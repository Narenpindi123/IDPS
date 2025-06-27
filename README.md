# 🛡️ Intrusion Detection System (IDS) – SYN Flood Detection

This Python-based IDS monitors real-time network traffic to detect SYN flood attacks. It uses **Scapy** to analyze packets, **Flask** to display logs in a web interface, and **iptables** to block attacker IPs. Email alerts are also sent when an attack is detected.

---

## 🚀 Features

- ✅ Detects SYN flood attacks using **Scapy**
- 🌐 Live attack logs via a **Flask web dashboard**
- 📧 Sends **email alerts** upon detection
- 🔒 Automatically **blocks attacker IPs** using iptables
- 📁 Downloads logs in **JSON format**
- 🧾 Ignores trusted IPs like `127.0.0.1`

---

## ⚙️ How It Works

1. Scapy monitors network packets.
2. If multiple SYN packets come from the same IP quickly, it’s flagged as an attack.
3. The system:
   - Logs the attack in a JSON file
   - Sends an email alert
   - Blocks the attacker IP via iptables
4. The Flask dashboard displays all detected events and allows log download.

---

## 🗂️ Project Structure

IDS/
├── ids_main.py # Main detection and web server logic
├── config.ini # Email configuration file
├── templates/
│ └── dashboard.html # HTML template for the dashboard
└── static/
└── intrusion_log.json # Stored attack logs

---

## 🧪 Setup Instructions

1. **Install dependencies**

```bash
pip install flask scapy
2. **Create a config.ini file**
[EMAIL]
sender = your_email@gmail.com
password = your_email_app_password
receiver = your_email@gmail.com
📌 Use an app-specific password if you're using Gmail.