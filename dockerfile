# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies
RUN pip install --no-cache-dir flask numpy opencv-python-headless

# Expose the port your app runs on
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=server.py

# Run server.py when the container launches
CMD ["python", "server.py"]

