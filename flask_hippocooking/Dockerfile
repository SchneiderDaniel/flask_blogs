# Use the official Python image
FROM python:3.12-alpine

# Install bash and other necessary packages
RUN apk add --no-cache bash python3-dev build-base linux-headers pcre-dev nano ttf-dejavu

# Create the log directory
RUN mkdir -p /var/log/uwsgi

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and uWSGI configuration file into the container
COPY . .

# Expose the port on which uWSGI will run
EXPOSE 5001

# Start uWSGI with the .ini configuration file
CMD ["uwsgi", "--ini", "uwsgi.ini"]
