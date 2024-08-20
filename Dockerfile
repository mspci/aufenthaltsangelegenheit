# to build this image:
# docker build -t aufenthaltsangelegenheit-script .
# to run the docker container:
# docker run -d --name aufenthaltsangelegenheit-script aufenthaltsangelegenheit-script

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Geckodriver
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz" -O geckodriver.tar.gz && \
    tar -xzf geckodriver.tar.gz -C /usr/local/bin/ && \
    rm geckodriver.tar.gz

# Set the working directory
WORKDIR /app

# Copy the requirements file (if any) and install the Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script and any necessary files to the Docker container
COPY . /app

# Ensure the correct file permissions
RUN chmod +x /app/main.py

# Set the entrypoint command to run your script
#CMD ["python", "main.py"]
CMD ["tail", "-f", "/dev/null"]
