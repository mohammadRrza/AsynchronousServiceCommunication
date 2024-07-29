# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY consumer/requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the consumer directory into the container
COPY consumer /app

# Define the command to run the consumer script
CMD ["python", "consumer.py"]