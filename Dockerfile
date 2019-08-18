# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN tar -xzf pickle.tar.gz && rm pickle.tar.gz

# Define environment variable
ENV NAME sandbox

ENV FLASK_APP main.py
# Run main.py when the container launches


CMD ["python", "main.py"]
