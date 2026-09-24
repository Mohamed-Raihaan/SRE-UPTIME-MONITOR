# Automated URL Uptime Monitor & Alerting System

## 📌 Project Overview
A lightweight, automated Site Reliability Engineering (SRE) agent designed to continuously monitor web platform availability and instantly route critical failure alerts to operational communication channels (Discord/Slack). This project focuses on minimizing **Mean Time to Detection (MTTD)** through proactive alerting.

## 🛠️ Tech Stack & Architecture
* **Language:** Python 3 (Requests, JSON packages)
* **Automation:** Linux Crontab (Scheduled Daemon)
* **Alerting Pipe:** Webhooks API integration
* **Hosting:** Microsoft Azure Ubuntu VM

## 🚀 Setup & Automation Steps
1. **Script Placement:** The `monitor.py` script is hosted natively within the Ubuntu environment.
2. **Webhook Mapping:** Configured a Discord webhook token to act as the primary operational incident response center.
3. **Cron Scheduling:** Automated the script execution loop to run every 5 minutes using the Linux time-based job scheduler:
   ```bash
   */5 * * * * /usr/bin/python3 /home/ubuntu/monitor.py >> /home/ubuntu/monitor.log 2>&1
   ```

## 🚨 Incident Response & Runbook
* **Healthy State (200 OK):** Script logs standard telemetry metrics directly to `/home/ubuntu/monitor.log` without firing external notifications.
* **Failure State (Non-200 / Network Crash):** Instantly triggers a payload to the operational channel containing the timestamp, target domain, and HTTP failure code (e.g., 403 Forbidden, 500 Internal Error) for rapid debugging.
