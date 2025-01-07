import psutil
import subprocess
import time
import logging

def restart_laravel_service():
    try:
        logging.info("CPU usage exceeded 80%. Restarting Laravel service...")
        subprocess.run(["sudo", "systemctl", "restart", "lemonade-laravel-backend-service"], check=True)
        logging.info("Laravel service restarted successfully.")
    except subprocess.CalledProcessError as error:
        logging.info(f"Error restarting Laravel service: {error}")

def monitor_cpu_usage():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage percentage over 1 second
        logging.info(f"Current CPU usage: {cpu_usage}%")

        if cpu_usage > 80:
            restart_laravel_service()

        time.sleep(60)
if __name__ == "__main__":
    logging.info("Starting CPU usage monitor...")
    monitor_cpu_usage()
