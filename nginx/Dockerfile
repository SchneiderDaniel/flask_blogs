# Use the official NGINX base image
FROM nginx:1.27.2


# Install the nginx-extras package and OpenSSL
RUN apt-get update && \
    apt-get install -y nginx-extras && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG ENVIRONMENT=prd

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx_dev.conf to the Nginx configuration directory as nginx.conf
COPY nginx_${ENVIRONMENT}.conf /etc/nginx/nginx.conf

# Copy the script to the container
COPY init_nginx.sh /init_nginx.sh
RUN chmod +x /init_nginx.sh

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Set the entrypoint
ENTRYPOINT ["/init_nginx.sh"]
