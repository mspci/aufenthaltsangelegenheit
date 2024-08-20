import logging
import pickle
import time
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

WEBPAGE_URL = "INSERT WEB PAGE URL"
FALLBACK_URL = "INSERT FALLBACK URL"
GECKODRIVER_PATH = '/usr/local/bin/geckodriver'
COOKIE_FILE = 'cookies.pkl'
NOTIFICATION_URL = "INSERT NOTIFICATION URL"
PROFILE_PATH = './selenium_profile'

# Set up logging with timestamps
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def send_notification(message):
    try:
        response = requests.post(NOTIFICATION_URL, data=message.encode('utf-8'))
        if response.status_code == 200:
            logger.info("Notification sent successfully.")
        else:
            logger.warning(f"Failed to send notification. Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"An error occurred while sending notification: {str(e)}")


def add_save_cookies_button(driver):
    """Adds a button in the browser window to save cookies."""
    save_cookies_script = """
    var button = document.createElement('button');
    button.innerHTML = 'Save Cookies';
    button.style.position = 'fixed';
    button.style.top = '10px';
    button.style.right = '10px';
    button.style.padding = '10px';
    button.style.zIndex = '10000';
    document.body.appendChild(button);
    button.onclick = function() {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/save_cookies', true);
        xhr.send();
    };
    """
    driver.execute_script(save_cookies_script)


def save_cookies(driver):
    """Saves cookies to a file."""
    with open(COOKIE_FILE, 'wb') as f:
        pickle.dump(driver.get_cookies(), f)
    logger.info("Cookies saved successfully.")


try:
    # Set up the Firefox options
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('-profile')
    options.add_argument(PROFILE_PATH)

    # Set up the service
    service = Service(GECKODRIVER_PATH)

    logger.info("Initializing Firefox driver...")
    driver = webdriver.Firefox(service=service, options=options)

    # Load the page and set cookies
    logger.info("Opening page...")
    driver.get(WEBPAGE_URL)

    logger.info("Loading cookies from file...")
    try:
        with open(COOKIE_FILE, 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except FileNotFoundError:
        logger.warning("No cookies file found. Continuing without loading cookies.")

    # Flag to track whether the "No slots available" notification has been sent
    no_slots_notification_sent = False

    # Main loop to keep checking for available slots
    while True:
        logger.info("Reloading the page with cookies...")
        driver.get(WEBPAGE_URL)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        logger.info("Page loaded successfully. Checking for available slots...")

        # Check if an error message is displayed
        error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Es ist ein Fehler aufgetreten')]")
        if error_elements:
            logger.error("An error occurred: 'Es ist ein Fehler aufgetreten'. Redirecting to the homepage.")

            # Redirect to the fallback URL
            driver.get(FALLBACK_URL)

            # Add a button to save cookies after the user navigates to the desired page
            add_save_cookies_button(driver)

            logger.info("Please navigate to the desired page. Click 'Save Cookies' once you've reached the intended state.")

            # Wait indefinitely until the user saves the cookies
            while True:
                # Simulate server-side listener to save cookies (placeholder for button's action)
                if driver.current_url == FALLBACK_URL:
                    save_cookies(driver)
                    logger.info("Please restart the script after saving the cookies.")
                    break
            break  # Exit the loop since we need to restart the script
        else:
            # Check if no slots are available
            no_slots_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Kein freier Termin verfügbar')]")
            if no_slots_elements:
                if not no_slots_notification_sent:
                    current_time = datetime.now().strftime("%H:%M %d/%m/%Y")
                    message = "⚠️ No slots available at the moment. \n⏳ Checking every 60 seconds...\n\nGenerated at: {current_time}"
                    logger.info(message)
                    send_notification(message)
                    no_slots_notification_sent = True
                logger.info("No slots available. Reloading in 60 seconds...")
                time.sleep(60)  # Wait for 60 seconds before retrying
            else:
                # Slots are available
                current_time = datetime.now().strftime("%H:%M %d/%m/%Y")
                message = f"🎉 Slots available! Hurry and book your appointment now! 🚀\n\nBook here: {WEBPAGE_URL}\n\nGenerated at: {current_time}"
                logger.info(message)
                send_notification(message)
                break  # Exit the loop when slots are found

except Exception as e:
    logger.error(f"An error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        logger.info("Script completed.")
        # logger.info("Closing the browser...")
        # driver.quit()
    else:
        logger.warning("Driver was not initialized.")

logger.info("Script terminated.")
