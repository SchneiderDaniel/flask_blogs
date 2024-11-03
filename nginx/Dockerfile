# Use the official NGINX base image
FROM nginx:1.22.1

# Install the nginx-extras package and OpenSSL
RUN apt-get update && \
    apt-get install -y nginx-extras openssl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx_dev.conf to the Nginx configuration directory as nginx.conf
COPY nginx_dev.conf /etc/nginx/nginx.conf

# Copy the script to the container
COPY init-letsencrypt.sh /init-letsencrypt.sh
RUN chmod +x /init-letsencrypt.sh

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Set the entrypoint
ENTRYPOINT ["/init-letsencrypt.sh"]
