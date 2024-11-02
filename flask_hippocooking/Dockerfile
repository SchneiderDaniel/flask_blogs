# Use the official Python image
# Use the official Python image
FROM python:3.12-alpine

# Install bash and other necessary packages
RUN apk add --no-cache bash python3-dev build-base linux-headers pcre-dev

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and uWSGI configuration file into the container
COPY . .

# Expose the port on which uWSGI will run
EXPOSE 5000

# Start uWSGI with the .ini configuration file
CMD ["uwsgi", "--ini", "uwsgi.ini"]
