import psutil
import curses
import smtplib
import logging
from email.mime.text import MIMEText
from time import sleep

# Configure logging for debugging and monitoring
logging.basicConfig(filename="sysguardian.log", level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to send an email alert
def send_email_alert(subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'your_email@example.com'  # Change to your email address
        msg['To'] = 'admin@example.com'  # Change to your recipient's email address

        with smtplib.SMTP('smtp.example.com') as server:  # Change to your SMTP server
            server.starttls()
            server.login('your_email@example.com', 'password')  # Change to your email credentials
            server.sendmail('your_email@example.com', 'admin@example.com', msg.as_string())
            logging.info(f"Email alert sent: {subject}")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

# Function to get system information (CPU, memory, processes)
def get_system_info():
    try:
        cpu_usage = psutil.cpu_percent(interval=.5)
        memory = psutil.virtual_memory()
        processes = []

        for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                cpu_percent = p.info['cpu_percent']
                if cpu_percent is not None:
                    processes.append((p.info['pid'], p.info['name'], cpu_percent))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        processes.sort(key=lambda x: x[2], reverse=True)
        return cpu_usage, memory.percent, processes

    except Exception as e:
        logging.error(f"Error in get_system_info: {e}")
        return 0, 0, []

# Function to get network information
def get_network_info():
    try:
        connections = psutil.net_connections(kind='inet')
        suspicious_connections = []

        for conn in connections:
            if conn.status == 'ESTABLISHED' and conn.raddr:
                suspicious_connections.append(conn)

        return suspicious_connections
    except Exception as e:
        logging.error(f"Error in get_network_info: {e}")
        return []

# Function to get disk usage information
def get_disk_info():
    try:
        disk_io = psutil.disk_io_counters()
        return disk_io.read_bytes, disk_io.write_bytes
    except Exception as e:
        logging.error(f"Error in get_disk_info: {e}")
        return 0, 0

# Function to display the information using curses
def display_info(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(1000)  # Update every second

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        # Get system information
        cpu_usage, memory_usage, processes = get_system_info()
        network_connections = get_network_info()
        disk_read, disk_write = get_disk_info()

        # Clear the screen to update information
        stdscr.clear()

        # Display general system stats
        stdscr.addstr(0, 0, f"CPU Usage: {cpu_usage}%")
        stdscr.addstr(1, 0, f"Memory Usage: {memory_usage}%")
        stdscr.addstr(2, 0, f"Disk Read: {disk_read / 1024**2:.2f} MB | Disk Write: {disk_write / 1024**2:.2f} MB")

        # Display top 5 processes by CPU usage
        stdscr.addstr(4, 0, "Top Processes by CPU Usage:")
        for i, (pid, name, cpu) in enumerate(processes[:5]):
            stdscr.addstr(5 + i, 2, f"{name} (PID: {pid}) - {cpu}% CPU")
            if cpu > 80:  # Alert for high CPU usage
                stdscr.addstr(5 + i, 2, f"{name} (PID: {pid}) - {cpu}% CPU", curses.color_pair(1))
                send_email_alert("High CPU Usage", f"Process {name} (PID: {pid}) is using {cpu}% CPU.")

        # Display suspicious network connections
        stdscr.addstr(10, 0, "Suspicious Network Connections:")
        for i, conn in enumerate(network_connections[:5]):
            stdscr.addstr(11 + i, 2, f"Local: {conn.laddr} -> Remote: {conn.raddr}")
            if conn.raddr.ip.startswith('192.168.') == False:  # Example condition: foreign IP
                stdscr.addstr(11 + i, 2, f"Local: {conn.laddr} -> Remote: {conn.raddr}", curses.color_pair(1))
                send_email_alert("Suspicious Network Activity", f"Suspicious network connection: {conn.laddr} -> {conn.raddr}")

        # Handle user input: press 'q' to quit
        key = stdscr.getch()
        if key == ord('q'):
            break

        # Refresh the screen to display updated information
        stdscr.refresh()

# Main function
def main():
    try:
        curses.wrapper(display_info)
    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
