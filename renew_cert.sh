#!/bin/bash

# Define log directory and clean up old logs
LOGDIR="/var/log"
LOGPREFIX="certbot_renew_"
find "$LOGDIR" -name "${LOGPREFIX}*.log" -type f -delete

# Create new log file with current timestamp
LOGFILE="${LOGDIR}/${LOGPREFIX}$(date '+%Y%m%d_%H%M%S').log"

{
    echo "Starting certificate renewal at $(date)"

    # Execute certbot with automatic 'yes' to renew
    docker exec certbot /bin/sh -c "
        echo '2' | certbot certonly --webroot -w /var/www/certbot -d hippocooking.com -d www.hippocooking.com
    "

    echo "Restarting Docker services..."
    cd /root/flask_blogs || { echo 'Failed to change directory'; exit 1; }
    docker-compose restart

    echo "Certificate renewal completed at $(date)"
} &> "$LOGFILE"
