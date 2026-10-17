def check_if_email_exists_in_facebook_via_selenium_webdriver(email: str = '', driver=None, quit: bool = False) -> dict:
    """
    Checks if a Facebook account exists for the given email by attempting a login via Selenium WebDriver.
    Handles common login responses and errors, including missing email, incorrect password, or account not found.

    Args:
        email (str): Email address to check. (Defaults to '')
        driver (Any): Selenium WebDriver instance used to automate the browser.
        quit (bool): Whether to quit the WebDriver after the check. (Defaults to False)

    Returns:
        dict: Dictionary with keys:
            - 'error' (str | None): Error message if an exception occurs, or None.
            - 'status_code' (int | None): HTTP status code of the network response if retrievable, else None.
            - 'message' (str | None): Text from the page describing the login response.
            - 'available' (int | None): 1 if email not linked to any account, 0 if account exists, None if unknown.

    Example usage:
        >>> result = check_if_email_exists_in_facebook_via_selenium_webdriver(email='user@example.com', driver=my_driver, quit=True)
    	"""

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    def get_status_code(driver, url_part="facebook.com"):
        import json
        logs = driver.get_log("performance")

        for entry in logs:
            message = json.loads(entry["message"])["message"]

            if message["method"] == "Network.responseReceived":
                response = message["params"]["response"]

                if url_part in response["url"]:
                    return response["status"]

        return None

    if not email or not isinstance(email,str) or not email.strip():
        return {"error": 'email missing', "status_code": get_status_code(driver, url_part=driver.current_url) if driver else None, "message": None, 'available': None}

        #options = Options()
        #options.add_argument("--headless")
        #driver = webdriver.Chrome(options=options)
        #driver = SetDriver()# should use the already set driver
    try:
        driver.get("https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=100")
        wait = WebDriverWait(driver, 10)
    except Exception as e1:
        return {"error": str(e1), "status_code": get_status_code(driver, url_part=driver.current_url), "message": None, 'available': None}


    try:
        cookie_card = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div._al67"))
            )
        #print("Cookie card appeared.")

        element = driver.find_element(By.CSS_SELECTOR, '[data-testid="cookie-policy-manage-dialog"]')
        if element:
            driver.execute_script("arguments[0].remove();", element)


    except Exception as ee:
        return {"error":'Unknown error!'+str(ee), "status_code": get_status_code(driver, url_part=driver.current_url), "message": None, 'available': None}
        #print('card not found')
    # Find the element with the specific class
    try:
            # Enter email
        email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#email")))
        email_field_value = email_field.get_attribute("value")
        email_field.clear()
        email_field.send_keys(email)
    except Exception as e2:
        return {"error": str(e2), "status_code": get_status_code(driver, url_part=driver.current_url), "message": None, 'available': None}
    try:
        button = wait.until(EC.presence_of_element_located((By.ID, "loginbutton")))
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        driver.execute_script("arguments[0].click();", button)
    except Exception as e3:
        return {"error": str(e3), "status_code": get_status_code(driver, url_part=driver.current_url), "message": None, 'available': None}
    time.sleep(2)  # Wait for response
    try:

        if 'https://www.facebook.com/two_step_verification/authentication/?encrypted_context' in driver.current_url:
            return {"error":  'captcha error', "status_code": get_status_code(driver, url_part=driver.current_url), "message": None, 'available': None}
    except Exception as e2a:
        return {"error": str(e2a), "status_code": get_status_code(driver, url_part=driver.current_url), "message": None, 'available': None}

    try:
        error_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._9ay7")))
        error_text = error_element.text
    except Exception as e2:
        return {"error": str(e2), "status_code": get_status_code(driver, url_part=driver.current_url), "message": None, 'available': None}
    try:

        if error_text.strip() == 'The email you entered isn’t connected to an account. Create a new Facebook account.':
            return {"error": None, "status_code": get_status_code(driver, url_part=driver.current_url), "message": error_text.strip(), 'available': 1}
        elif 'The password you’ve entered is incorrect.' in error_text.strip():
            return {"error": None, "status_code": get_status_code(driver, url_part=driver.current_url), "message": error_text.strip(), 'available': 0}
        else:
            return {"error":'unknown error.', "status_code": get_status_code(driver, url_part=driver.current_url), "message": error_text.strip(), 'available': None}
    except Exception as e4:
        return {"error": str(e4), "status_code": get_status_code(driver, url_part=driver.current_url), "message": None, 'available': None}

    if driver and quit:
        driver.quit()



class FacebookChecker:
    def __init__(self, email: str = None, driver=None, quit=False):
        self.email = email.strip() if email else None
        self.source = 'facebook.com'
        call = check_if_email_exists_in_facebook_via_seleniuum(email=self.email, driver=driver, quit=quit)
        self.error = call['error']
        self.status_code = call['status_code']
        self.message = call['message']
        self.available = call['available']

    def __repr__(self):
        return f"{self.available}"

  