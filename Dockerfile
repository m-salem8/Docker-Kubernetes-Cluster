FROM ubuntu:20.04

# Install system dependencies
RUN apt update && apt install -y python3-pip libmysqlclient-dev mysql-client

# Copy your application files
ADD requirements.txt main.py ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port 8000 for your FastAPI application
EXPOSE 8000

# Start your FastAPI application using uvicorn
CMD uvicorn main:server --host 0.0.0.0 --port 8000