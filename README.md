# Hippocooking Homepage

## Python Cheatsheet

### Installation
------------

You should create a virtual environment and install the required packages with the following commands:

    windows:
    cd flask_hippocooking
    python -m venv env
    .\env\Scripts\activate    
    pip install -r requirements.txt

    Linux:
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

### Run
cd flask_hippocooking
.\env\Scripts\activate   
python run.py

or 

.\run_dev_server.bat


## Docker Cheatsheet

### Build the Docker Image
`docker build --no-cache -t flask_hippocooking --progress=plain . `

### Run the Docker Container
`docker run -d -p 5001:5001 -v ./logs:/var/log flask_hippocooking`  

### Stop
`docker stop container_name_or_id`

### Remove a Container
`docker rm container_name_or_id`

### View Running Containers
`docker ps`

### View all Containers
`docker ps -a`

### List Docker Images
`docker images`

### View Container Logs
`docker logs container_name_or_id`

### Enter a Running Container (using an interactive shell)
`docker exec -it container_name_or_id /bin/bash`

### Call Service
`curl -v http://localhost:8080`

### What service are running
`ss -tuln`

### Run python silent in docker to test
`python run.py > /dev/null 2>&1 &`

## Docker Compose Cheatsheet

### buidl and run with force

`docker-compose up --build --force-recreate`


docker-compose down
docker-compose up -d

http://localhost:5000/?lang=de


# Cert
docker exec -it certbot /bin/sh
certbot certonly --webroot -w /var/www/certbot -d hippocooking.com -d www.hippocooking.com
exit