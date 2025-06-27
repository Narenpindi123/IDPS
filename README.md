<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Intrusion Detection System (IDS) – SYN Flood Detection</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      max-width: 800px;
      margin: 2rem auto;
      padding: 0 1rem;
      color: #333;
    }
    h1, h2 {
      color: #005a9c;
    }
    ul, ol {
      margin-left: 1.5rem;
    }
    pre {
      background: #f4f4f4;
      padding: 1rem;
      overflow-x: auto;
    }
    code {
      font-family: Consolas, "Courier New", monospace;
      background: #f4f4f4;
      padding: 0.2rem 0.4rem;
      border-radius: 3px;
    }
    hr {
      border: none;
      border-top: 1px solid #ddd;
      margin: 2rem 0;
    }
  </style>
</head>
<body>

  <h1>🛡️ Intrusion Detection System (IDS) – SYN Flood Detection</h1>
  <p>This Python-based IDS monitors real-time network traffic to detect SYN flood attacks. It uses <code>Scapy</code> for packet analysis, <code>Flask</code> for a web dashboard, and <code>iptables</code> to block malicious IPs. Email alerts are sent on detection.</p>

  <hr>

  <h2>🚀 Features</h2>
  <ul>
    <li>Detects SYN flood attacks using <code>Scapy</code></li>
    <li>Live attack logs via a <code>Flask</code> web dashboard</li>
    <li>Sends email alerts upon detection</li>
    <li>Automatically blocks attacker IPs with <code>iptables</code></li>
    <li>Stores logs in JSON format</li>
    <li>Ignores trusted IPs (e.g. <code>127.0.0.1</code>)</li>
  </ul>

  <hr>

  <h2>🧠 How It Works</h2>
  <p>
    <strong>Scapy</strong> listens on the specified network interface for TCP SYN packets. When a single source IP exceeds the configured SYN threshold within a short time window, the system:
  </p>
  <ol>
    <li>Logs the event (timestamp, source IP, destination port) to a JSON file.</li>
    <li>Sends an email alert to the configured address.</li>
    <li>Blocks the attacker IP using <code>iptables</code>.</li>
    <li>Displays all events in a live <code>Flask</code> dashboard with log download capability.</li>
  </ol>

  <hr>

  <h2>📁 Project Structure</h2>
  <pre><code>IDS/
├── ids_main.py              # Main detection & web server logic
├── config.ini               # Email & detection settings
├── templates/
│   └── dashboard.html       # HTML template for the Flask dashboard
└── static/
    └── intrusion_log.json   # JSON file storing attack logs
  </code></pre>

  <hr>

  <h2>⚙️ Setup Instructions</h2>
  
  <ol>
    <li>
      <strong>Install dependencies:</strong><br>
      <pre><code>pip install flask scapy</code></pre>
    </li>
    <li>
      <strong>Create <code>config.ini</code> in the project root:</strong><br>
      <pre><code>[EMAIL]
sender   = your_email@gmail.com
password = your_email_app_password
receiver = your_email@gmail.com

[DETECTION]
syn_flood_threshold = 10
alert_rate_limit    = 60
block_threshold     = 20
      </code></pre>
      <p><em>Use an app-specific password if you're using Gmail.</em></p>
    </li>
    <li>
      <strong>Run the IDS:</strong><br>
      <pre><code>sudo python3 ids_main.py</code></pre>
    </li>
    <li>
      <strong>Open the dashboard:</strong><br>
      <code>http://127.0.0.1:5000</code> (or <code>http://&lt;your-ip&gt;:5000</code>)
    </li>
  </ol>

  <hr>

  <h2>🧪 Simulate a SYN Flood Attack</h2>
  <p>From another machine on the same network, run:</p>
  <pre><code>sudo hping3 -S -p 5000 -a 192.168.1.99 --flood 10.0.2.15</code></pre>
  <p>This sends a high-rate SYN flood spoofed from <code>192.168.1.99</code> to your IDS at <code>10.0.2.15</code>.</p>

  <hr>

  <h2>🧹 Reset & Cleanup</h2>
  <ul>
    <li><strong>Stop flood attacks:</strong> <code>sudo pkill hping3</code></li>
    <li><strong>Clear logs:</strong> <code>sudo rm static/intrusion_log.json</code></li>
    <li><strong>Flush firewall rules:</strong> <code>sudo iptables -F</code></li>
  </ul>

  <hr>

  <h2>📬 Example Email Alert</h2>
  <pre><code>Subject: IDS Alert
Body: Alert: SYN flood from 192.168.1.99 at 2025-06-27 17:26:16
  </code></pre>

  <hr>

  <h2>📄 License</h2>
  <p>Released under the <strong>MIT License</strong>. Free to use, modify, and distribute for educational and research purposes.</p>

</body>
</html>
