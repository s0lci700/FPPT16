# Use an official Python image as the base image
FROM python:3.11.4

# Set environment variables to avoid Python bytecode and buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for your app
RUN apt-get update && \
    apt-get install -y nodejs npm

# Create a directory for your application and set it as the working directory
RUN mkdir /code
WORKDIR /code

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Node.js and npm
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# Copy the package.json and package-lock.json files to install npm dependencies
COPY package*.json /code/
RUN npm install

# Copy the rest of your Django application code
COPY . /code/

# Copy the Django secret key file into the container
COPY django_secrets.env /code/


# Expose the port your app runs on (you may need to adjust this to your Django settings)
EXPOSE 8000

# Start the application using the start.sh script and read the secret key from the file
CMD ["sh", "-c", "export $(cat /code/django_secrets.env | xargs) && /code/start.sh"]
