# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port that the API will listen on
EXPOSE 8000

# Specify the command to run your API using uvicorn (adjust the module and port as needed)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]