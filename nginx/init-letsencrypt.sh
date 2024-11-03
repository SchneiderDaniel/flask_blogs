#!/bin/bash

if [ ! -f /etc/letsencrypt/live/localhost.crt ]; then
    mkdir -p /etc/letsencrypt/live/
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/letsencrypt/live/localhost.key \
        -out /etc/letsencrypt/live/localhost.crt \
        -subj "/CN=localhost"
fi

# Start NGINX
exec nginx -g 'daemon off;'