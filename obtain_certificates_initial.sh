#!/bin/bash

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
mkdir -p ./nginx_volume/certbotlogs

# Adjust permissions on the webroot
sudo chown -R $USER:$USER ./nginx_volume/certbot ./nginx_volume/ssl ./nginx_volume/certbotlogs

# Install Certbot if it's not already installed
if ! command -v certbot &> /dev/null; then
    echo "Installing Certbot..."
    sudo apt install certbot -y
fi

## Cert
docker run -it --rm -v ./nginx_volume/ssl:/etc/letsencrypt  \
-v ./nginx_volume/ssl-dhparams:/etc/ssl/certs  \
-v ./nginx_volume/certbot:/var/www/certbot  \
-v ./nginx_volume/certbotlogs:/var/log/letsencrypt  \
-p 80:80  \
certbot/certbot \
certonly  --standalone --preferred-challenges http

# Check if the command succeeded
if [ $? -eq 0 ]; then
    echo "Certificates obtained successfully. You can now use the certificates located in ./nginx_volume/ssl."
else
    echo "Failed to obtain certificates. Please check the logs above."
    exit 1
fi