# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8082

#COPY .env /app/.env
# Run Django commands and start the application
#CMD ["sh", "-c", "python manage.py makemigrations --no-input && \
#                   python manage.py migrate --no-input && \
#                   python manage.py runserver 0.0.0.0:8082"]



CMD ["sh", "-c", "python manage.py migrate --no-input && \
                  python manage.py runserver 0.0.0.0:8082"]
