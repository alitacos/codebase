# not working as expected , does not have good structure, logic, ,leads to error ****it does not do is thescribed to do...
 

import psutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_chrome_running():
    """Check if Chrome is running by looking at the process list."""
    for proc in psutil.process_iter(['pid', 'name']):
        if 'chrome' in proc.info['name'].lower():
            return True
    return False

def attach_to_chrome():
    """Attach to an existing Chrome session using remote debugging."""
    chrome_options = Options()
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--headless")  # Optional: If you want headless mode, remove this if visible
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def check_for_google_tab(driver):
    """Check all open tabs for google.com"""
    tabs = driver.window_handles
    for tab in tabs:
        driver.switch_to.window(tab)
        if "google.com" in driver.current_url:
            print(f"Google tab found: {driver.current_url}")
            return True
    print("No Google tab found!")
    return False

def wait_for_captcha_and_privacy(driver):
    """Wait for CAPTCHA and privacy settings to be solved manually."""
    print("Please solve CAPTCHA and accept privacy settings manually.")
    
    while True:
        try:
            # Check for CAPTCHA (if present)
            driver.find_element(By.XPATH, '//*[@id="captcha"]')
            time.sleep(2)
        except:
            break
    
    # Wait for privacy settings (cookies consent) to be solved
    while True:
        try:
            # Look for cookies consent popup and wait
            driver.find_element(By.XPATH, '//*[@id="L2AGLb"]')  # Cookies consent accept button
            time.sleep(2)
        except:
            break
    
    print("CAPTCHA and privacy settings solved, continuing with extraction...")

def extract_search_results(driver, query):
    """Extract search results after query."""
    try:
        # Wait for the search box to be visible
        search_box = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "APjFqb"))
        )
        
        # Clear and input the query
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for the results to load
        time.sleep(3)
        
        # Extract the search result links
        results = driver.find_elements(By.XPATH, '//h3//a')
        return [(result.text, result.get_attribute("href")) for result in results[:5]]  # Get top 5 results
    except Exception as e:
        print(f"Error during result extraction: {e}")
        return []

def monitor_browser_and_extract():
    """Main function to monitor and extract search results from an open browser."""
    if not is_chrome_running():
        print("Chrome is not running. Start Chrome manually.")
        return

    driver = attach_to_chrome()
    
    # Wait for the browser to be fully ready and try detecting the open tab
    time.sleep(3)
    
    # Check if Google is already open in any tab
    if check_for_google_tab(driver):
        wait_for_captcha_and_privacy(driver)
        
        queries = ["OpenAI", "GPT-4", "Selenium Python"]
        
        for query in queries:
            print(f"Processing query: {query}")
            results = extract_search_results(driver, query)
            for title, url in results:
                print(f"Result: {title} - {url}")
    else:
        print("No Google tab found!")
    
    # Close the driver after operations
    driver.quit()

# Run the browser monitoring and extraction process
monitor_browser_and_extract()
