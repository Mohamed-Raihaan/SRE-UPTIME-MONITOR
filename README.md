# Project 1: Automated URL Uptime Monitor & Alerting System

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




# 📊 Project 2: Cloud Telemetry, Log Analytics & Observability

## 📌 Project Overview
Implemented cloud-native observability across infrastructure by streaming live system performance metrics into a centralized data lake. This project focuses on establishing platform visibility and tracking performance anomalies using enterprise monitoring solutions.

## 🛠️ Architecture & Data Pipeline
* **Telemetry Collector:** Azure Monitor Agent (AMA) installed on Ubuntu Linux
* **Log Aggregator:** Azure Log Analytics Workspace
* **Query Language:** Kusto Query Language (KQL)
* **Visualization:** Azure Metrics Dashboard

## 🔍 Incident Simulation & KQL Analysis
To test the logging pipeline’s responsiveness to a platform failure, a CPU load spike was artificially generated within the VM using the Linux `stress` utility:
```bash
sudo apt-get install -y stress
stress --cpu 2 --timeout 60s
```

The metric anomaly was targeted, queried, and isolated inside the Azure Workspace using the operational query saved in `cpu_alert_query.kql`.

## 📈 Outcome
Successfully captured and mapped the real-time resource spike on a live telemetry graph, which was pinned to a central operational dashboard for instant infrastructure health tracking.




# 💾 Project 3: Automated Disaster Recovery & Data Retention

## 📌 Backup Architecture
To prevent permanent data loss during a critical infrastructure crash, an automated shell script (`backup.sh`) runs via a system cron daemon every night at midnight (`0 0 * * *`). The script packages live application code and active telemetry configurations into compressed binaries (`.tar.gz`) stored in an isolated volume path.

## 🧹 Retention Policy
To prevent volume storage exhaustion alerts, the script executes automated clean-up logic loop using standard Linux find operations:
```bash
find "$BACKUP_DIR" -type f -name "sre_app_backup_*.tar.gz" -mtime +7 -exec rm {} \;
```
This safely purges any archival artifacts older than 7 days, ensuring total disk storage stability.

## 🚨 EMERGENCY RUNBOOK: Infrastructure Restoration Protocol
*In the event of a total virtual machine failure or OS corruption, follow these recovery steps:*

1. **Provision Infrastructure:** Spin up a clean Ubuntu Linux instance on Azure.
2. **Retrieve Latest Archive:** Fetch the latest `sre_app_backup_TIMESTAMP.tar.gz` from the backup pool.
3. **Extract Payload:** Execute the extraction command to restore application state:
   ```bash
   tar -xzf sre_app_backup_FILENAME.tar.gz -C /home/azureuser/
   ```
4. **Re-initialize Automated Services:** Restore the cron schedules by running `crontab -e` and appending the monitoring and backup job parameters.
5. **Verify Endpoint Health:** Confirm system restoration by running the local monitoring agent manually.
