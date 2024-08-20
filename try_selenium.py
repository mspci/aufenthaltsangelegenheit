import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Set up the Firefox options
    options = Options()

    # Set the new profile path
    # Remove the following three lines to let Selenium
    # create a temporary profile for each run.
    # Conventional profile paths:
    # Windows: C:\Users\<username>\AppData\Roaming\Mozilla\Firefox\Profiles\<profile>
    # Linux: /home/$USER/.mozilla/firefox/<profile>
    # Linux: /home/$USER/snap/firefox/common/.mozilla/firefox/<profile>
    # enter 'about:support' in the Firefox address bar to find the profile path
    # in the 'Profile Directory' field
    # or enter 'about:profiles' in the Firefox address bar to find the profile path
    profile_path = '$USER/snap/firefox/common/.mozilla/firefox/selenium'
    options.add_argument('-profile')
    options.add_argument(profile_path)

    # Set up the service
    service = Service('/usr/local/bin/geckodriver')

    logger.info("Initializing Firefox driver...")
    driver = webdriver.Firefox(service=service, options=options)

    logger.info("Opening Google...")
    driver.get("https://www.google.com")

    # Wait for the search box to be present
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    logger.info("Google search page loaded successfully.")

except Exception as e:
    logger.error(f"An error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        logger.info("Closing the browser...")
        driver.quit()
    else:
        logger.warning("Driver was not initialized.")

logger.info("Script completed.")
