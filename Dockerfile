# Use an official Python runtime as a parent image
FROM python:3.13.2

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the application runs on (modify as needed)
EXPOSE 4444

# Define the command to run the application (modify as needed)
CMD ["python", "main.py"]