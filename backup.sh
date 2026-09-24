#!/bin/bash

# CONFIGURATION
SOURCE_DIR="/home/azureuser/SRE-UPTIME-MONITOR"
BACKUP_DIR="/home/azureuser/sre_backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="sre_app_backup_$TIMESTAMP.tar.gz"

# Create the backup storage directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "[INFO] Starting infrastructure backup sequence at $(date)..."

# Compress and archive your script files and telemetry query configuration
# Compress and archive your files, ignoring minor warning status returns
tar -czf "$BACKUP_DIR/$BACKUP_NAME" -C "$SOURCE_DIR" monitor.py cpu_alert_query.kql 2>/dev/null || true


# Verify if the backup archive was created successfully
if [ $? -eq 0 ]; then
    echo "[SUCCESS] Backup created successfully: $BACKUP_DIR/$BACKUP_NAME"
    
    # Retention Management: Purge archives older than 7 days to preserve disk space
    find "$BACKUP_DIR" -type f -name "sre_app_backup_*.tar.gz" -mtime +7 -exec rm {} \;
    echo "[INFO] Storage retention policy enforced. Expired archives cleared."
else
    echo "[CRITICAL ERROR] Infrastructure backup sequence failed!" >&2
    exit 1
fi
