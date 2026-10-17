def check_if_element_is_disabled_in_selenium_webdriver_page()->bool:
from selenium.webdriver.common.by import By

button = driver.find_element( By.XPATH, "//div[@role='button'][.//span[normalize-space()='Continue' or normalize-space()='Weiter']]" )
if button:
    button.click()
disabled = ( button.get_attribute("disabled") is not None or button.get_attribute("aria-disabled") == "true" )

print(disabled)