# 🛡️ SysGuardian

A comprehensive system monitoring and security tool that provides real-time visibility into system resources, network connections, and potential security threats.

## 🔍 Overview

The Enhanced System Monitor combines system resource tracking with security monitoring capabilities. It's designed for system administrators, security professionals, and anyone who needs visibility into their system's performance and security status.

## ✨ Features

### System Monitoring
- **CPU usage tracking** - Real-time CPU utilization metrics
- **Memory monitoring** - Track available and used RAM
- **Process analysis** - Identify top CPU-consuming processes
- **Disk I/O statistics** - Monitor read/write operations

### Security Features
- **Network connection monitoring** - Track established network connections
- **Suspicious connection detection** - Highlight potentially concerning connections
- **Automated email alerts** - Get notified of high CPU usage and suspicious activity
- **Activity logging** - Maintain detailed logs of system events

### User Experience
- **Color-coded alerts** - Visual indicators of potential issues
- **Simple terminal UI** - Easy-to-read interface using curses
- **Configurable email notifications** - Stay informed even when away

## 📋 Requirements

- Python 3.6 or higher
- Required Python packages:
  - `psutil` - For system resource monitoring
  - `curses` - For terminal UI (included in standard Python)
  - Access to an SMTP server for email alerts

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/sysguardian.git
   cd sysguardian
   ```

2. Install required packages:
   ```bash
   pip install psutil
   ```

3. Configure email settings:
   Open `sysguardian.py` and update the following in the `send_email_alert()` function:
   ```python
   msg['From'] = 'your_email@example.com'  # Your email address
   msg['To'] = 'admin@example.com'  # Recipient's email address
   with smtplib.SMTP('smtp.example.com') as server:  # Your SMTP server
       server.starttls()
       server.login('your_email@example.com', 'password')  # Your credentials
   ```

## 💻 Usage

Run the enhanced monitor:
```bash
python sysguardian.py
```

### Controls
- **q** - Quit the application
- The display refreshes automatically every second

### Alert Thresholds

The system is configured to alert on:
- Processes using more than 80% CPU
- Network connections to non-local IP addresses (configured as non-192.168.* in the example)

## 📊 Monitoring Details

### System Metrics
- CPU usage percentage
- Memory usage percentage
- Disk read/write activity in MB

### Security Monitoring
- Active network connections
- Remote IP addresses
- Potentially suspicious connections

## 📝 Logging

All monitoring activities, alerts, and errors are logged to `sysguardian.log`, including:
- Email alerts sent
- System errors encountered
- Connection and process monitoring events

## 🛠️ Customization

You can customize the monitoring thresholds by modifying:
- CPU alert threshold (default: 80%)
- Suspicious network connection criteria
- Email alert frequency

## 🔒 Security Considerations

- Store email credentials securely
- Run with appropriate permissions to access process information
- Be aware that network monitoring may have privacy implications

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for legitimate system monitoring and security purposes only. Always ensure you have proper authorization before monitoring systems, especially network connections.
