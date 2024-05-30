FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
RUN pip install --upgrade pip
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Expose the port on which the application will run
EXPOSE 8000

# Copy the application code to the working directory
COPY . .

# Run App
CMD ["fastapi", "run", "main.py", "--port", "8000"]
