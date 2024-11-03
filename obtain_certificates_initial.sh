#!/bin/bash

# Define your domain and email here
DOMAIN="hippocooking.com"  # Replace with your actual domain
EMAIL="daniel.schneider.privat@googlemail.com"  # Replace with your actual email

# Function to install Docker
install_docker() {
    echo "Installing Docker..."

    # Update the package index
    sudo apt update && sudo apt upgrade -y

    # Install necessary packages
    sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

    # Add Docker’s official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    # Add the Docker repository
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

    # Install Docker
    sudo apt update
    sudo apt install docker-ce -y

    # Start and enable Docker
    sudo systemctl start docker
    sudo systemctl enable docker

    echo "Docker installed successfully."
}

# Function to install Docker Compose
install_docker_compose() {
    echo "Installing Docker Compose..."

    # Download the latest version of Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    # Set permissions
    sudo chmod +x /usr/local/bin/docker-compose

    echo "Docker Compose installed successfully."
}

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    install_docker
fi

if ! command -v docker-compose &> /dev/null; then
    install_docker_compose
fi

# Create the necessary directories for the webroot
mkdir -p ./nginx_volume/certbot
mkdir -p ./nginx_volume/ssl

# Adjust permissions on the webroot
sudo chown -R $USER:$USER ./nginx_volume/certbot ./nginx_volume/ssl

# Run the Certbot command to obtain the SSL certificates
docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot \
  -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --no-eff-email --force-renewal

# Check if the command succeeded
if [ $? -eq 0 ]; then
    echo "Certificates obtained successfully. You can now run docker compose."
else
    echo "Failed to obtain certificates. Please check the logs above."
    exit 1
fi
