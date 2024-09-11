# locators.py
from selenium.webdriver.common.by import By

# XPath and ID locators for elements
locators = {
    'google_oauth_button': (By.XPATH, '//*[@id="idp1"]'),  # Targeting the Google OAuth button
    'email_input': (By.ID, 'identifierId'),  # Input field for the email
    'next_button': (By.ID, 'identifierNext'),  # Button to proceed after entering email
    'password_input': (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'),  # Input field for the password
    'password_next_button': (By.ID, 'passwordNext'),  # Button to proceed after entering password
    'status_dropdown': (By.XPATH, "//div[@class='ant-select-selector']"),
    'new_option': (By.XPATH, "//div[@class='ant-select-item-option-content' and text()='New']"), 
    'contacted_option': (By.XPATH, "//div[@class='ant-select-item-option-content' and text()='Contacted']"), 
    'pending_credit_option': (By.XPATH, "//div[@class='ant-select-item-option-content' and text()='Pending Credit App']"), 
    'app_completed_option': (By.XPATH, "//div[@class='ant-select-item-option-content' and text()='App Completed']"), 
    'rejected_option': (By.XPATH, "//div[@class='ant-select-item-option-content' and text()='Rejected']"), 
    'search_button': ((By.XPATH, "//button//span[text()='Search']")), # Renamed 'New' to 'new_option'
    'status_column': (By.XPATH, "//td[contains(@class, 'tabulator-cell') and @data-column='status']"),
    'next': ((By.XPATH, "//button[@class='tabulator-page' and @aria-label='Next Page']")),
}
