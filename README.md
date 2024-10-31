 Intrusion Detection System (IDS) with Python and Flask
Overview
This project is a simple Intrusion Detection System (IDS) built in Python that detects SYN flood attacks. It logs detected intrusions, displays them on a web dashboard using Flask, and can send email alerts for suspicious activities. The IDS can also automatically block malicious IPs by modifying firewall rules with `iptables`.
Features
- Real-time Packet Sniffing: Monitors incoming network traffic to detect SYN flood attacks.
- SYN Flood Detection: Detects SYN flood attacks based on a configurable threshold.
- IP Blocking: Automatically blocks IPs involved in SYN flood attacks using `iptables`.
- Email Alerts: Sends email alerts for detected intrusions (configurable).
- Web Dashboard: Displays intrusion logs on a real-time web dashboard built with Flask.
- JSON Logging: Logs intrusion details in a JSON format for easy parsing and analysis.

Requirements
- Python 3
- scapy - for packet sniffing and network analysis
- flask - for web dashboard
- hping3 (for testing purposes) - for generating SYN flood traffic
- iptables (for IP blocking on Linux systems)

Python Libraries
Install required libraries:
pip install scapy flask

Configuration
Create a config.ini file in the project directory to specify email settings and detection thresholds.
Example config.ini:
ini
[email]
sender = your_email@example.com
receiver = alertreceiver@example.com
password = your_password

[detection]
syn_flood_threshold = 10  # Number of SYN packets to detect a flood
alert_rate_limit = 60     # Minimum time (seconds) between email alerts for the same IP
block_threshold = 20      # Number of SYN packets to trigger IP blocking
Usage
Running the IDS
1.	Start the IDS:
Cmd: sudo python3 ids_main.py
The IDS will:
o	Start sniffing for network packets.
o	Detect SYN flood attacks based on the threshold set in config.ini.
o	Log intrusions to intrusion_log.json.
o	Start a Flask web server to display intrusion logs.
2.	Access the Web Dashboard:
Open a web browser and navigate to:
arduino
http://127.0.0.1:5000
This will display a dashboard showing recent intrusion events.
Testing SYN Flood Detection
To simulate a SYN flood attack (for testing purposes only), use hping3 from another terminal:
Cmd: sudo hping3 -S -p 80 --flood <target_ip>
Replace <target_ip> with the IP address of the machine running the IDS.
Stopping SYN Flood Testing
To stop the SYN flood attack, press Ctrl + C in the terminal running hping3.
Alternatively, if hping3 is running as a background process, you can find and kill it with:
Cmd: ps aux | grep hping3
sudo kill <PID>
Project Structure:
├── ids_main.py          # Main IDS code
├── config.ini           # Configuration file for email and detection settings
├── intrusion_log.json   # JSON file where detected intrusions are logged
├── README.md            # Documentation file
└── templates/
    └── index.html       # HTML template for the web dashboard
How It Works
1.	Packet Sniffing: The IDS uses scapy to capture incoming packets and analyzes TCP flags to identify SYN packets.
2.	SYN Flood Detection: When the number of SYN packets from a single IP exceeds the threshold, the IDS logs the activity and sends an email alert if configured.
3.	IP Blocking: If the SYN flood threshold continues to increase, the IDS can automatically block the source IP with iptables.
4.	Web Dashboard: Logs are displayed in real-time on a Flask-based web dashboard.
Screenshots
Web Dashboard
Console Output
Notes
•	Running as Root: Because scapy requires low-level network access, the IDS must be run with root privileges.
•	Testing: SYN flood attacks can disrupt network services. Run tests in a controlled environment and do not target external networks.
•	Security: This IDS is for educational purposes. In production, a more robust solution like a firewall or a dedicated IDS/IPS is recommended.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments
•	Built with scapy for packet sniffing and network analysis.
•	Flask for creating the web dashboard.
•	iptables for firewall rules and IP blocking on Linux.
________________________________________
Feel free to contribute and open issues to improve this project!

---

Instructions for Use

1. Copy the content above and save it as `README.md` in your project directory.
2. Replace `URL-to-image` with links to screenshots of your web dashboard and console output if you'd like to include visuals on GitHub.
3. Customize the sections as needed for your specific setup or requirements.
