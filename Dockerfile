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

# Install matching ChromeDriver version based on installed Chrome
# Install matching ChromeDriver version based on installed Chrome
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') \
    && CHROME_MAJOR_VERSION=$(echo "$CHROME_VERSION" | cut -d'.' -f1) \
    && CHROMEDRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | grep -oP '"version": "\d+\.\d+\.\d+\.\d+"' | head -1 | grep -oP '\d+\.\d+\.\d+\.\d+') \
    && wget -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /usr/local/bin/chromedriver-linux64 \
    && chmod +x /usr/local/bin/chromedriver

# Set working directory in container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app/

# Set environment variable for the port; Render sets $PORT at runtime
ENV PORT=10000

# Command to run Gunicorn server, note app module changed from app_1 to app
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:$PORT", "app:app"]
