# Use the official Python 3.11 slim image as base
FROM python:3.11-slim

# Install Chrome and its dependencies, then clean apt cache to reduce image size
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    fonts-liberation \
    libnss3 \
    libfontconfig1 \
    libgtk-3-0 \
    libx11-xcb1 \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome official signing key and repository, then install Chrome stable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory in container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# --> Add this line to copy your application code into the container.
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]