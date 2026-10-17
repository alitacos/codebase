def check_pinterest_email_exists_via_selenium(email=None,driver=None,quit=False):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    import time
    if not driver:
        quit = True
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

    message = None  # Initialize message
    try:
        driver.get("https://de.pinterest.com/password/reset/")
        wait = WebDriverWait(driver, 15)

        # Click login modal button
        login_modal_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#__PWS_ROOT__ > div:nth-child(3) > div:nth-child(2) > div.QLY._he.p6V.zI7.iyn.Hsu > div > div.Eqh.Jea.KS5.s7I.zI7.iyn.Hsu > div.H-G.zI7.iyn.Hsu > button > div > div"
        )))
        login_modal_button.click()

        # Enter email
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#email")))
        email_input.clear()
        email_input.send_keys(email)

        # Click submit
        submit_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#__PWS_ROOT__ > div:nth-child(3) > div:nth-child(5) > div > div > div > div > div > div.KS5.jzS.un8.C9i.TB_ > div:nth-child(1) > form > div.qGb.zI7.iyn.Hsu > button > div > div"
        )))
        submit_button.click()

        time.sleep(2)  # Wait for response

        # Look for error messages
        for selector in [
            ('div[data-test-id="touchableErrorMessage"]', "general"),
            ("#email-error", "email"),
            ("#password-error", "password")
        ]:
            try:
                error_element = driver.find_element(By.CSS_SELECTOR, selector[0])
                message = ' '.join(error_element.text.strip().split())
                break  # Stop on first found error
            except:
                continue

        if message == 'The email you entered does not belong to any account.':
            return {"error": None, "status_code": 200, "message": message, 'available': 1}
        elif  'The password you entered is incorrect. Try again or Reset your password' or 'We noticed some strange activity on your account.' in message :
            return {"error": None, "status_code": 200, "message": message, 'available': 0}
        elif 'You have exceeded your rate limit' in message:
            return {"error": message, "status_code": 200, "message": None, 'available': None}
        
            
        else:
            return {"error": message, "status_code": 200, "message": None, 'available': None}
        if quit:
            driver.quit()

    except Exception as e:
        if 'invalid session id' in str(e):
            return check_pinterest_email_exists_via_selenium(email=email,driver=None,quit=False)
        else:        
            return {"error": str(e), "status_code": None, "message": None, 'available': None}
        if driver and quit:
            driver.quit()

class PinterestChecker:
    def __init__(s, email: str = None, driver=None,quit=False):
        s.email = email.strip() if email else None
        s.source = 'pinterest.com'
        call = check_pinterest_email_exists_via_selenium(email=s.email,driver=None,quit=False) if not driver else check_pinterest_email_exists_via_selenium(email=s.email,driver=driver)
        s.error = call['error']
        s.status_code = call['status_code']
        s.message = call['message']
        s.available = call['available']

    def __repr__(s):
        return str(s.available)


#example usage:
#pinterest = PinterestChecker(email='anjikjkujbzvtvtv@gmail.com',quit=False,driver=None )
#pinterest.__dict__