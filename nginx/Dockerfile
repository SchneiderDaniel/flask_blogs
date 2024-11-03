# Use the official NGINX base image
# Use the latest stable version of the official Ubuntu image
FROM ubuntu:24.04

# Install dependencies and NGINX with extras
RUN apt-get update && \
    apt-get install -y nginx-extras openssl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ARG ENVIRONMENT=prd

# Copy custom nginx_dev.conf to the Nginx configuration directory as nginx.conf
COPY nginx_${ENVIRONMENT}.conf /etc/nginx/nginx.conf

# Copy the script to the container
COPY init_nginx.sh /init_nginx.sh
RUN chmod +x /init_nginx.sh

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Set the entrypoint
ENTRYPOINT ["/init_nginx.sh"]
