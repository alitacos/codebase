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
    def get_facebook_cookie_buttons(driver, timeout=5):
        """
        Ensure on Facebook login page.
        Return a dict {'accept': WebElement or None, 'decline': WebElement or None}
        Finds buttons with aria-label containing 'cookies' (case-insensitive).
        Does NOT assume presence of 'allow' or 'decline' in aria-label.
        """
        FACEBOOK_LOGIN_URL = "https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=100"
        # 1. Make sure we are on Facebook login page
        try:
            if "facebook.com/login" not in driver.current_url:
                driver.get(FACEBOOK_LOGIN_URL)
        except Exception:
            driver.get(FACEBOOK_LOGIN_URL)
        # 2. Wait shortly for cookie banner dialog presence
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]')))
        except TimeoutException:
            # No cookie dialog at all
            return {'accept': None, 'decline': None}

        # 3. Find all clickable buttons where aria-label contains 'cookies' (case-insensitive)
        # XPath: translate to lowercase to do case-insensitive contains
        xpath_cookies_buttons = ('//div[@role="button" and contains(translate(@aria-label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "cookies")]')
        try:
            buttons = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, xpath_cookies_buttons)))
        except TimeoutException:
            return {'accept': None, 'decline': None}
        # 4. Separate accept vs decline buttons heuristically:
        # We'll check aria-label text for words like 'allow' or 'decline' (case-insensitive),
        # but if not present, assign None for that type.
        accept_btn = None
        decline_btn = None
        for btn in buttons:
            aria = btn.get_attribute("aria-label").lower()
            if "allow" in aria or "erlauben" in aria:
                accept_btn = btn
            elif "decline" in aria or "ablehnen" in aria:
                decline_btn = btn
        return {'accept': accept_btn, 'decline': decline_btn}


    
        
        
        
    print(check_facebook_cookie_banner(driver))
    if check_facebook_cookie_banner(driver):
        buttons = get_facebook_cookie_buttons(driver)
        print(buttons)
        if buttons:
            if accept and buttons['accept']:
                driver.execute_script("arguments[0].click();", buttons['accept'])
                print("Clicked Accept button.")
            elif not accept and buttons['decline']:
                driver.execute_script("arguments[0].click();", buttons['decline'])
                print("Clicked Decline button.")
            else:
                print("No appropriate button found.")
        else:
            print("No cookie buttons found.")
    else:
        print("No cookie banner detected.")
#check_cookies_permissions_on_facebook_login_page(driver,accept=False)
#### no nothing happend. the button is still there