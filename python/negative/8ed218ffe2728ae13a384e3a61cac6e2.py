from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def check_cookies_permissions_on_facebook_login_page(driver=None, accept=False, timeout=5):
    FACEBOOK_LOGIN_URL = "https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=100"

    def check_facebook_cookie_banner(driver, timeout=timeout):
        try:
            current_url = driver.current_url
        except Exception:
            current_url = ""

        if "https://www.facebook.com/login/" not in current_url:
            driver.get(FACEBOOK_LOGIN_URL)

        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]'))
            ) or WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]'))
            )
            return True
        except TimeoutException:
            return False

    def get_cookies_buttons(driver, timeout=timeout):
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]'))
            )
        except TimeoutException:
            return {'accept': None, 'decline': None}

        xpath_cookies_buttons = (
            '//div[@role="button" and contains(translate(@aria-label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "cookies")]'
        )
        try:
            elements = WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath_cookies_buttons))
            )
        except TimeoutException:
            return {'accept': None, 'decline': None}

        # We will try to differentiate accept/decline buttons by aria-label text (lowercase)
        accept_button = None
        decline_button = None
        for el in elements:
            aria_label = el.get_attribute('aria-label')
            if not aria_label:
                continue
            aria_label_lower = aria_label.lower()
            if 'allow' in aria_label_lower or 'accept' in aria_label_lower:
                accept_button = el
            elif 'decline' in aria_label_lower or 'reject' in aria_label_lower:
                decline_button = el

        return {'accept': accept_button, 'decline': decline_button}

    if check_facebook_cookie_banner(driver):
        buttons = get_cookies_buttons(driver)
        if buttons:
            if accept and buttons['accept']:
                try:
                    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(buttons['accept']))
                    buttons['accept'].click()
                    print("Clicked Accept button.")
                except TimeoutException:
                    print("Accept button not clickable.")
            elif not accept and buttons['decline']:
                try:
                    # Use JavaScript to scroll into view and remove potential overlays
                    driver.execute_script("arguments[0].scrollIntoView(true);", buttons['decline'])
                    driver.execute_script("arguments[0].click();", buttons['decline'])  # Use JS click
                    print("Clicked Decline button.")
                except TimeoutException:
                    print("Decline button not clickable.")
            else:
                print("No appropriate button found.")
        else:
            print("No cookie buttons found.")
    else:
        print("No cookie banner detected.")


#check_cookies_permissions_on_facebook_login_page(driver)