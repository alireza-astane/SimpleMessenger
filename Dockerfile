FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered output.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory.
WORKDIR /app

# Install system dependencies.
RUN apt-get update && apt-get install -y gcc

# Copy requirements.txt first and install dependencies.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the remainder of the project.
COPY . .

# Expose the FastAPI port.
EXPOSE 8000

# Set the default CMD to run the FastAPI app.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]