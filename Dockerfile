# Use an official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Create a Python virtual environment
ENV VIRTUAL_ENV=/app/venv
RUN python -m venv $VIRTUAL_ENV

# Ensure the virtual environment is used for all subsequent commands
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Set the default command to run the app
CMD ["python", "tekk-tools/arthurgpt/app.py"]