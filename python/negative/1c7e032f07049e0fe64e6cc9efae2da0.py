def start_driver_and_visit_url_page_via_selenium_driver_and_return_driver(url: str='', driver: 'selenium.webdriver'=None, headless=True) -> bool:
    if not url:
        return driver if driver else None
    import time
    if not driver:
        options = Options()
        if headless:
            options.add_argument('headless')
        options.add_argument('no-sandbox')
        options.add_argument('disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-setuid-sandbox')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3)
    return driver