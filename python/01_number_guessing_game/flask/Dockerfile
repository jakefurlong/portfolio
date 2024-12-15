# Use the official Python image as a base
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first (for caching)
COPY app/requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip --no-cache-dir --root-user-action=ignore \
    && pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Copy the rest of the application files
COPY app/ .

# Expose the application port
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py"]
