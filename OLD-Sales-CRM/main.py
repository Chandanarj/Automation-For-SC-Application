import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from config import credentials, base_url
from locators import locators

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    logging.info("Setting up the ChromeDriver.")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)  # Implicit wait to allow elements to load
    return driver

def login(driver):
    try:
        logging.info("Navigating to the website.")
        driver.maximize_window()
        driver.get(base_url)
        
        logging.info("Performing Google OAuth login.")
        google_oauth_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(locators['google_oauth_button']))
        google_oauth_button.click()
        
        logging.info("Entering email address.")
        email_input = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(locators['email_input']))
        email_input.send_keys(credentials['email'])
        driver.find_element(*locators['next_button']).click()
        
        logging.info("Entering password.")
        password_input = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(locators['password_input']))
        password_input.send_keys(credentials['password'])
        driver.find_element(*locators['password_next_button']).click()

    except Exception as e:
        logging.error(f"An error occurred during login: {e}")
        driver.save_screenshot('error_screenshot_login.png')
        driver.quit()
        raise

def select_status_and_search(driver, status_value, status_locator_key):
    try:
        logging.info(f"Accessing the status dropdown and selecting '{status_value}'.")
        dropdown_element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(locators['status_dropdown']))
        dropdown_element.click()

        logging.info(f"Selecting the '{status_value}' status.")
        status_option = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locators[status_locator_key]))
        status_option.click()

    except Exception as e:
        logging.error(f"Failed to select status '{status_value}': {e}")
        driver.save_screenshot(f'error_select_status_{status_value}.png')
        raise

def scroll_and_click_search(driver):
    try:
        logging.info("Scrolling to and clicking the Search button.")
        search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locators['search_button']))
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
        time.sleep(2)
        search_button.click()

    except Exception as e:
        logging.error(f"Failed to click the Search button: {e}")
        driver.save_screenshot('error_search_button.png')
        raise

def scroll_to_top(driver):
    logging.info("Scrolling to the top of the page.")
    driver.execute_script("window.scrollTo(0, 0);")  # Scroll to the top

def scroll_to_bottom(driver):
    logging.info("Scrolling to the bottom of the page.")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom

def check_status_column(driver, expected_status):
    try:
        logging.info(f"Checking the status column for '{expected_status}' values.")
        statuses = driver.find_elements(*locators['status_column'])
        
        for status in statuses:
            if status.text != expected_status:
                logging.error(f"Found a non-{expected_status} status: {status.text}")
                return False
        logging.info(f"All rows in the Status column are '{expected_status}'.")
        return True

    except Exception as e:
        logging.error(f"An error occurred while checking the status column for '{expected_status}': {e}")
        driver.save_screenshot(f'error_check_status_{expected_status}.png')
        return False

def click_next_button(driver, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            # Check if the Next button is available
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locators['next']))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", next_button)
            time.sleep(1)  # Wait for any dynamic content to load
            actions = ActionChains(driver)
            actions.move_to_element(next_button).click().perform()
            logging.info("Next button clicked successfully.")
            return True
        except StaleElementReferenceException:
            logging.warning(f"StaleElementReferenceException: Retrying to click the Next button, attempt {attempt + 1}")
            attempt += 1
            time.sleep(1)
        except Exception as e:
            logging.warning("Next button not found, assuming it's the last page.")
            return False  # No more pages, exit loop

    return False  # If retries exhausted

def process_all_pages(driver, expected_status, total_pages=20):
    current_page = 1
    while current_page <= total_pages:
        logging.info(f"Processing page {current_page}/{total_pages} for status '{expected_status}'.")

        # Scroll to the top of the page and check the status
        scroll_to_top(driver)
        if check_status_column(driver, expected_status):
            logging.info(f"Top of page {current_page} checked successfully for '{expected_status}'.")
        else:
            logging.error(f"Non-{expected_status} status found in top section of page {current_page}.")
            break
        
        # Scroll to the bottom of the page and check the status
        scroll_to_bottom(driver)
        if check_status_column(driver, expected_status):
            logging.info(f"Bottom of page {current_page} checked successfully for '{expected_status}'.")
        else:
            logging.error(f"Non-{expected_status} status found in bottom section of page {current_page}.")
            break

        # Click Next button if there are more pages, otherwise break
        if not click_next_button(driver):
            logging.info(f"No more pages for status '{expected_status}'. Stopping.")
            break
        
        current_page += 1

def process_status(driver, status_value, status_locator_key):
    select_status_and_search(driver, status_value, status_locator_key)
    scroll_and_click_search(driver)
    process_all_pages(driver, expected_status=status_value)

def main():
    driver = setup_driver()
    try:
        login(driver)
        
        # Process for each status sequentially
        status_list = [
            ('New', 'new_option'),
            ('Contacted', 'contacted_option'),
            ('Pending Credit App', 'pending_credit_option'),
            ('App Completed', 'app_completed_option'),
            ('Rejected', 'rejected_option')
        ]
        
        for status_value, status_locator_key in status_list:
            logging.info(f"Starting process for status '{status_value}'.")
            process_status(driver, status_value, status_locator_key)
        
        logging.info("Process completed successfully for all statuses.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info("Closing the driver.")
        driver.quit()

if __name__ == "__main__":
    main()
