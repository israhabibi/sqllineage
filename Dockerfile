# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Set environment variable to tell Flask to run in production mode
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
