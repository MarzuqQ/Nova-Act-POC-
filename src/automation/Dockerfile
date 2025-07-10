FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Set working directory
WORKDIR /app

# Install system dependencies for browser automation
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    gnupg \
    unzip \
    xvfb \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxss1 \
    libgconf-2-4 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies (Nova Act will handle Playwright internally)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create results directory
RUN mkdir -p /app/results

# Set permissions
RUN chmod -R 755 /app

# Set environment variables for headless mode
ENV DISPLAY=:99
ENV HEADLESS=true

# Default environment variables (can be overridden)
ENV PORTAL_URL=http://vendor-portal:5000
ENV PORTAL_USERNAME=shipping_admin
ENV PORTAL_PASSWORD=secure_pass123
ENV TIMEOUT=300

# Wait script to ensure portal is ready
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Run the automation
CMD ["sh", "-c", "echo 'Waiting for vendor portal to be ready...' && sleep 15 && python3 main.py"] 