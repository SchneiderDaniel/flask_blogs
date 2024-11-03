#!/bin/bash

# Define your domain and email here
DOMAIN="hippocooking.com"  # Replace with your actual domain
EMAIL="daniel.schneider.privat@googlemail.com"  # Replace with your actual email

# Check if the user is running the script with Docker Compose installed
if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null
then
    echo "Docker and Docker Compose must be installed to run this script."
    exit 1
fi

# Create the necessary directories for the webroot
mkdir -p ./nginx_volume/certbot

# Run the Certbot command to obtain the SSL certificates
docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot \
  -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --no-eff-email

# Check if the command succeeded
if [ $? -eq 0 ]; then
    echo "Certificates obtained successfully. You can now run docker compose."
else
    echo "Failed to obtain certificates. Please check the logs above."
    exit 1
fi
