# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update and install system libraries
RUN apt-get update && apt-get install -y \
    ghostscript \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Set the default port as an environment variable
ENV PORT=8000

# Expose the port defined by the environment variable
EXPOSE $PORT

# Run the uvicorn command with the PORT environment variable
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
