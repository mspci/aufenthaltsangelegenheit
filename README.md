# 🚀 Appointment Checker Script

This script automates the process of checking for available appointments on a specified website. It uses Selenium to interact with the site, continuously checking for available slots and sending notifications when slots become available.

## 🛠️ Environment Setup

To ensure the script runs smoothly, you need the following:

- **Python Version**: `3.12.4`
- **OS**: Ubuntu 24.04
- **Selenium WebDriver**: Firefox with Geckodriver

## 📋 Prerequisites

Before you begin, make sure you have the following installed and set up:

### 1. **Install Poetry** 📦

Poetry is used to manage Python dependencies for this project.

```bash
pipx install poetry
```

### 2. **Install Firefox** 🌐

Ensure Firefox is installed on your system. If not, install it using:

```bash
sudo snap install firefox
```

If you used `apt` to install Firefox, you'll need to modify the path to the default profile in `main.py:21`. Here are the paths to Firefox profiles:

- Ubuntu (Snap): `/home/$USER/snap/firefox/common/.mozilla/firefox/selenium`
- Ubuntu (APT): `/home/$USER/.mozilla/firefox/selenium`
- Windows: `C:\\Users\\$USER\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\selenium`

You can find the path to profiles by entering `about:profiles` or `about:support` in the Firefox address bar (look for "Profile Directory").

### 3. **Install Dependencies** 📂

Navigate to the project directory and install the necessary Python packages:

```bash
poetry install
```

### 4. **Install Geckodriver** 🧩

You can use the provided bash script `geckodriver_installer.sh` to install Geckodriver. This script downloads, extracts, and installs Geckodriver for you.

To run the script:

```bash
bash geckodriver_installer.sh
```

### 5. **Create a Selenium Profile** 🖥️

To ensure Selenium uses the correct Firefox profile, create a new profile:

```bash
firefox -no-remote -CreateProfile "selenium ${PWD}/selenium_profile"
```

## 🚀 Running the Script

Once everything is set up, you can run the script directly. It will continuously check for available appointment slots and send a notification if any slots are found.

```bash
poetry run python main.py
```

### GUI mode

If you need to manually debug the script by interacting with the browser, you can disable the headless mode. To do this, simply comment out the line in the script where headless mode is set (`main.py:70`):

```python
# options.add_argument("--headless")  # Comment this out to enable the browser UI for debugging
```

With this line commented out, the Firefox browser will open with a visible UI, allowing you to manually inspect and interact with the page while the script runs.

## 📬 Notifications

The script sends notifications using [ntfy.sh](https://ntfy.sh/). Make sure to update the `NOTIFICATION_URL` variable in the script if you need to change the notification endpoint.

## 📦 Development

If you plan to modify or further develop this script, the following Poetry commands may be useful:

- **Add a Dependency**: `poetry add <dependency>`
- **Install Dependencies**: `poetry install`
- **Export Requirements**: `poetry export -f requirements.txt -o requirements.txt`

Feel free to use these commands as you develop or modify the script.

## 🖥️ Using Chrome

If you prefer to use Chrome instead of Firefox, you'll need to modify the script and use ChromeDriver. Replace the Firefox WebDriver setup with Chrome and update the necessary options to point to the Chrome profile instead.

---
