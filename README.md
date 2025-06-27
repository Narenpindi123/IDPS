Intrusion Detection System (IDS) – SYN Flood Detection

This is a Python-based IDS that detects SYN flood attacks in real time. It monitors network traffic using Scapy, logs detected attacks, sends email alerts, blocks attacker IPs using iptables, and displays logs on a Flask-based web dashboard.

Features:

Detects SYN flood attacks using Scapy

Flask web dashboard for live attack logs

Sends email alerts on detection

Blocks attacker IP with iptables

Downloads logs in JSON format

Ignores trusted IPs like 127.0.0.1

How It Works:
Scapy captures packets on the network interface. If multiple SYN packets are detected from the same IP in a short time, the system logs it, sends an email alert, and blocks that IP using iptables. The Flask dashboard shows all activity and allows log downloads.

Project Structure:
IDS/
├── ids_main.py
├── config.ini
├── templates/dashboard.html
└── static/intrusion_log.json

Setup:

Install dependencies: pip install flask scapy

Create a config.ini file with the following:
[EMAIL]
sender = your_email@gmail.com
password = your_email_app_password
receiver = your_email@gmail.com

Run the IDS: sudo python3 ids_main.py

Open your browser and go to: http://127.0.0.1:5000

Simulate a SYN Flood Attack:
Use the following command from another system:
sudo hping3 -S -p 5000 -a 192.168.1.99 --flood 10.0.2.15

Reset or Cleanup:

Stop any hping3 process: sudo pkill hping3

Delete logs: sudo rm static/intrusion_log.json

Clear firewall rules: sudo iptables -F

Email Alert Sample:
Subject: IDS Alert
Body: Alert: SYN flood from 192.168.1.99 from 192.168.1.99

License:
MIT License – For educational use only