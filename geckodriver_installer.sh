#!/bin/bash

# Purpose: This script automates the process of downloading, extracting,
# and installing geckodriver on Ubuntu systems.

# Steps:
# 1. Download geckodriver from the GitHub release page
# 2. Extract the downloaded archive
# 3. Move the geckodriver binary to /usr/local/bin
# 4. Make the binary executable
# 5. Verify the installation
# 6. Remove the downloaded archive

# Set variables
GECKODRIVER_VERSION="v0.35.0"
GECKODRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz"
GECKODRIVER_ARCHIVE="geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz"

# Download geckodriver
echo "Downloading geckodriver..."
wget "$GECKODRIVER_URL"

# Extract the archive
echo "Extracting geckodriver..."
tar -xvzf "$GECKODRIVER_ARCHIVE"

# Move geckodriver to /usr/local/bin
echo "Moving geckodriver to /usr/local/bin..."
sudo mv geckodriver /usr/local/bin/

# Make geckodriver executable
echo "Making geckodriver executable..."
sudo chmod +x /usr/local/bin/geckodriver

# Verify the installation
echo "Verifying the installation..."
geckodriver --version

# Remove the downloaded archive
echo "Cleaning up..."
rm "$GECKODRIVER_ARCHIVE"


echo "Installation complete!"
