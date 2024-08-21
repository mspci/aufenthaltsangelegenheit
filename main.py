import logging
import os
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

WEBPAGE_URL = "INSERT WEB PAGE URL"
FALLBACK_URL = "INSERT FALLBACK URL"
GECKODRIVER_PATH = '/usr/local/bin/geckodriver'
COOKIE_FILE = 'cookies.pkl'
NOTIFICATION_URL = "INSERT NOTIFICATION URL"
PROFILE_PATH = '/home/INSERT USER HERE/snap/firefox/common/.mozilla/firefox/selenium'


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


def save_cookies(driver):
    """Saves cookies to a file."""
    with open(COOKIE_FILE, 'wb') as f:
        pickle.dump(driver.get_cookies(), f)
    logger.info("Cookies saved successfully.")


def load_cookies(driver):
    logger.info("Loading cookies from file...")
    try:
        with open(COOKIE_FILE, 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except FileNotFoundError:
        logger.warning("No cookies file found. Continuing without loading cookies.")


def navigate_to_webpage(driver):
    """Navigate through the web page to the desired location."""
    try:
        elements_to_click = [
            {"xpath": "//input[@id='cookie_msg_btn_no']", "name": "Cookie Message Button"},
            {"xpath": "//button[@id='buttonfunktionseinheit-1']", "name": "Funktionseinheit Button"},
            {"xpath": "//h3[@id='header_concerns_accordion-455']", "name": "Concerns Accordion"},
            {"xpath": "//button[@id='button-plus-286']", "name": "Plus Button"},
            {"xpath": "//input[@id='WeiterButton']", "name": "Weiter Button"},
            {"xpath": "//button[@id='OKButton']", "name": "OK Button"},
            {"xpath": "/html/body/main/div/details[2]/div/form/input[4]", "name": "Select Location"}
        ]

        for element in elements_to_click:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, element["xpath"]))).click()

        # Wait for the desired page to load
        WebDriverWait(driver, 5).until(EC.url_to_be(WEBPAGE_URL))
        logger.info("Successfully navigated to the desired page.")

    except Exception as e:
        logger.error(f"An error occurred while navigating: {str(e)}")

def initialize_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('-profile')
    options.add_argument(PROFILE_PATH)

    service = Service(GECKODRIVER_PATH)

    logger.info("Initializing Firefox driver...")
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def main():
    driver = None
    last_cookie_save_time = time.time()
    no_slots_notification_sent = False

    try:
        os.remove(COOKIE_FILE)
        logger.info("Cookies file removed.")
    except FileNotFoundError:
        pass

    while True:
        try:
            if not driver:
                driver = initialize_driver()

            logger.info("Opening page...")
            driver.get(WEBPAGE_URL)

            load_cookies(driver)

            while True:
                logger.info("Reloading the page with cookies...")
                driver.get(WEBPAGE_URL)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                logger.info("Page loaded successfully. Checking for available slots...")

                error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Es ist ein Fehler aufgetreten')]")
                if error_elements:
                    logger.info(f"Cookies are missing. \nRedirecting to {FALLBACK_URL}\nCookies will be saved automatically.")
                    driver.get(FALLBACK_URL)
                    navigate_to_webpage(driver)

                    if driver.current_url == WEBPAGE_URL:
                        save_cookies(driver)
                        load_cookies(driver)
                else:
                    no_slots_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Kein freier Termin verfügbar')]")
                    if no_slots_elements:
                        if not no_slots_notification_sent:
                            current_time = datetime.now().strftime("%H:%M %d/%m/%Y")
                            message = f"\n⚠️ No slots available at the moment. \n⏳ Checking every 60 seconds...\n\nGenerated at: {current_time}"
                            logger.info(message)
                            no_slots_notification_sent = True
                        logger.info("No slots available. Reloading in 60 seconds...")
                        time.sleep(60)
                    else:
                        date_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Montag,') or contains(text(), 'Dienstag,') or contains(text(), 'Mittwoch,') or contains(text(), 'Donnerstag,') or contains(text(), 'Freitag,') or contains(text(), 'Samstag,') or contains(text(), 'Sonntag,')]")

                        available_slots = []

                        for date_element in date_elements:
                            available_date = date_element.text
                            time_elements = date_element.find_elements(By.XPATH, ".//following-sibling::button")
                            available_times = [time.text for time in time_elements if time.is_enabled()]

                            if available_times:
                                available_slots.append((available_date, available_times))

                        if available_slots:
                            message_parts = []
                            for date, times in available_slots:
                                times_str = ", ".join(times)
                                message_parts.append(f"{date}: {times_str}")

                            message_body = "\n".join(message_parts)
                            current_time = datetime.now().strftime("%H:%M %d/%m/%Y")
                            message = f"🎉 Slots available!\n\n{message_body}\n\nBook here: {WEBPAGE_URL}\n\nGenerated at: {current_time}"
                            logger.info(message)
                            send_notification(message)
                            time.sleep(420)
                        else:
                            logger.info("No enabled time slots found.")

                current_time = time.time()
                if current_time - last_cookie_save_time >= 1200:
                    save_cookies(driver)
                    last_cookie_save_time = current_time

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            logger.info("Retrying in 60 seconds...")
            time.sleep(60)

        finally:
            if driver:
                logger.info("Quitting...")
                driver.quit()
                driver = None


if __name__ == "__main__":
    main()
    logger.info("Script terminated.")
