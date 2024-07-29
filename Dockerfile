# Use a lightweight Python base image
FROM python:3.8-buster
# Set the working directory in the container
WORKDIR /app


COPY requirements.txt .
RUN curl -I https://pypi.org
RUN pip install flask==3.0.3
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
CMD ["python", "app.py"]