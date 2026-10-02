# 1. Base Image: Use an official lightweight Python runtime
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Prevent Python from writing .pyc files and enable unbuffered output logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Install system dependencies (needed for installing certain Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy requirements first to leverage Docker's build cache
COPY requirements.txt .

# 6. Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the rest of the application code into the container
COPY . .

# 8. Expose Streamlit's default port (8501)
EXPOSE 8501

# 9. Healthcheck to verify the app is running smoothly
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 10. Entrypoint command to run the Streamlit app
ENTRYPOINT ["streamlit", "run", "sla_calculator.py", "--server.port=8501", "--server.address=0.0.0.0"]
