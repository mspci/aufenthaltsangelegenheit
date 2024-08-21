#!/bin/bash
set -e

if [ ! -d "/home/winter/snap/firefox/common/.mozilla/firefox/selenium" ]; then
  mkdir -p /home/winter/snap/firefox/common/.mozilla/firefox/selenium
fi

/usr/bin/firefox-esr -headless -no-remote -CreateProfile "selenium /home/winter/snap/firefox/common/.mozilla/firefox/selenium" || \
    firefox -headless -no-remote -CreateProfile "selenium /home/winter/snap/firefox/common/.mozilla/firefox/selenium"

python3 /app/main.py

#exec "$@"
