# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only the requirements file, to cache the pip install step
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Install Gunicorn for production
RUN pip install gunicorn

# Use Gunicorn to serve the app with Uvicorn workers. Adjust the number of workers as necessary.
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
