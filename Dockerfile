# Fetch the official Python 3.11 Image
FROM python:3.11.4

# Ensures Python outputs everything that's printed inside
# the application directly to the terminal (makes the Docker logs cleaner)
ENV PYTHONUNBUFFERED=1

# Python 3.14 is not currently available but 3.11.4 will mostly suit all the requirements

# Set evironment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Node.js is required for npm
# Install Node.js
RUN apt-get update && \
    apt-get install -y nodejs npm

# Create a directory for the application and set it as working directory
RUN mkdir /code
WORKDIR /code

# Install Django and other dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install npm dependencies
COPY package*.json /code/
RUN npm install

# Copy the entire Django application
COPY . /code/