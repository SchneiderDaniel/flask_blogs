# Build the Docker Image
`docker build -t flask_hippocooking . `

# Run the Docker Container
`docker run -d -p 8080:8080 -v ./logs:/tmp/ flask_hippocooking`

# Stop
`docker stop container_name_or_id`

# Remove a Container
`docker rm container_name_or_id`

# View Running Containers
`docker ps`

# View all Containers
`docker ps -a`

# List Docker Images
`docker images`

# View Container Logs
`docker logs container_name_or_id`

# Enter a Running Container (using an interactive shell)
`docker exec -it container_name_or_id /bin/bash`

# Call Service
`curl -v http://localhost:8080`

# What service are running
`ss -tuln`