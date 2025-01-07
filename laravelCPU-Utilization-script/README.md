# LARAVEL BACKEND RESTART ON CPU USAGE THRESHOLD OF 80%

This guide explains how to set up a Python script as a service on a server using **systemd**. The script monitors CPU usage and restarts the Laravel backend service if the CPU usage exceeds 80%.

---

## Prerequisites

1. **Python Installed**: Ensure Python 3 is installed on the server.
2. **psutil Library**: Install the `psutil` library using:
   ```bash
   pip install psutil
   ```
3. **Script File**: Save the Python script from this repository as `/usr/local/bin/restart_laravel_backend.py` on your server.

   Make the script executable:
   ```bash
   sudo chmod +x /usr/local/bin/restart_laravel_backend.py
   ```

---

## Steps to Set Up as a Systemd Service

### 1. Create a Systemd Service File

Create a new systemd service file:

```bash
sudo nano /etc/systemd/system/laravel_backend_cpu_monitor.service
```

Add the following content:

```ini
[Unit]
Description=Monitor CPU usage and restart Laravel service if CPU exceeds 80%
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/restart_laravel_backend.py
Restart=always
User=your_user
WorkingDirectory=/usr/local/bin
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=laravel_backend_cpu_monitor

[Install]
WantedBy=multi-user.target
```

### Key Points:
- **`ExecStart`**: Path to the Python interpreter and your script.
- **`Restart=always`**: Ensures the service restarts if it crashes.
- **`User=your_user`**: Replace `your_user` with the appropriate user (e.g., `root` or a specific system user).
- **`SyslogIdentifier`**: Sets a label for logs in `journalctl`.

---

### 2. Reload Systemd and Enable the Service

Reload systemd to recognize the new service file:

```bash
sudo systemctl daemon-reload
```

Enable the service to start on boot:

```bash
sudo systemctl enable laravel_backend_cpu_monitor.service
```

---

### 3. Start the Service

Start the service using the following command:

```bash
sudo systemctl start laravel_backend_cpu_monitor.service
```

---

### 4. Check Service Status

Verify the service is running:

```bash
sudo systemctl status laravel_backend_cpu_monitor.service
```

You should see output indicating the service is active. Logs from your script can be viewed using:

```bash
journalctl -u laravel_backend_cpu_monitor.service
```

---

### 5. Stop or Restart the Service

To stop or restart the service:

```bash
sudo systemctl stop laravel_backend_cpu_monitor.service
sudo systemctl restart laravel_backend_cpu_monitor.service
```

---

## Troubleshooting

- Ensure the Python script runs correctly by testing it manually:
  ```bash
  python3 /usr/local/bin/restart_laravel_backend.py
  ```
- Check the system logs for errors:
  ```bash
  journalctl -u laravel_backend_cpu_monitor.service
  ```

---

## Notes

- Replace `laravel-backend` in the script with the actual service name or restart command for your Laravel backend.
- Ensure the user specified in the service file has sufficient permissions to restart services.
