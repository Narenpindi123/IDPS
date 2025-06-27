Intrusion Detection System (IDS) – SYN Flood Detection

This Python-based IDS detects SYN flood attacks in real time. It monitors network traffic using Scapy, logs detected events, sends email alerts, blocks attacker IPs via iptables, and provides a Flask web dashboard to view and download logs.

Features:

Detects SYN flood attacks using Scapy

Live attack logs via a Flask web dashboard

Sends email alerts upon detection

Automatically blocks attacker IPs with iptables

Stores events in a JSON log file

Whitelists trusted IPs (for example, 127.0.0.1)

How It Works:

Scapy captures TCP SYN packets on the chosen network interface.

If a single source IP sends more than the configured SYN threshold in a short period:
a. The event (timestamp, source IP, destination port) is appended to intrusion_log.json
b. An email alert is sent to the configured receiver
c. The source IP is blocked using an iptables DROP rule

A Flask application serves a dashboard at http://127.0.0.1:5000 where all logged events are displayed and can be downloaded as JSON.

Setup:

Install required Python packages by running:
pip install flask scapy

Create a file named config.ini in the project root with these contents:
[EMAIL]
sender = your_email@gmail.com
password = your_app_specific_password
receiver = your_email@gmail.com

[DETECTION]
syn_flood_threshold = 10
alert_rate_limit = 60
block_threshold = 20

Start the IDS by running:
sudo python3 ids_main.py

Open your browser and navigate to:
http://127.0.0.1:5000

Testing a SYN Flood:
From another machine on the same network, simulate an attack with:
sudo hping3 -S -p 5000 -a 192.168.1.99 --flood 10.0.2.15
(Replace 192.168.1.99 with your attacker IP and 10.0.2.15 with the IDS host IP.)

Cleanup:

Stop the flood attack process: sudo pkill hping3

Remove the JSON log file: sudo rm static/intrusion_log.json

Flush all iptables rules: sudo iptables -F