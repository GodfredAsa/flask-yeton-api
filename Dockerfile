# DEVELOPMENT
FROM python:3.9-slim


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

RUN mkdir -p /app


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE  5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to run the Flask app
CMD ["python", "app.py"]

## USING DOCKER COMPOSE =========================
#FROM python:3.9-slim
#
## Set the working directory in the container
#WORKDIR /app
#
## Copy the current directory contents into the container
#COPY . /app
#
## Create data directory for SQLite
#RUN mkdir -p /app/data
#
## Install Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt
#
## Expose the port Flask runs on
#EXPOSE 5000
#
## Set environment variables for Flask
#ENV FLASK_APP=app.py
#ENV FLASK_ENV=production
#
## Command to run the Flask app
#CMD ["python", "app.py"]