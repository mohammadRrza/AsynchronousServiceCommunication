# Use a lightweight Python base image
FROM python:3.9-slim
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .
RUN curl -I https://pypi.org
RUN pip install flask==3.0.3
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code into the container
COPY . .


# Install Python dependencies

# Copy the rest of the application code into the container

# Ensure permissions for all files
RUN chmod -R 755 /app

# Set the entry point for the container to run your Python script
CMD ["python3", "consumer/consumer.py"]