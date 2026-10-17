# not working as expected , does not have good structure, logic, ,leads to error ****it does not do is thescribed to do...
#extract_search_results_of_google_in_a_structured_format
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BrowserAutomation:
    def __init__(self, debugging_port=9222):
        """ Initialize the browser connection via remote debugging. """
        
        # Setup Chrome options for connecting to existing browser
        chrome_options = Options()
        chrome_options.add_argument(f"--remote-debugging-port={debugging_port}")
        chrome_options.add_argument("--headless")  # Optional: to run headlessly, or remove this if you want a visible browser
        
        # Connect to the running Chrome instance
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def check_if_google_open(self):
        """ Check if google.com is open in any tab. """
        
        tabs = self.driver.window_handles
        
        # Iterate through all open tabs to check for google.com
        for tab in tabs:
            self.driver.switch_to.window(tab)
            if "google.com" in self.driver.current_url:
                print("Google tab found!")
                return True
        return False
        
    def wait_for_captcha_and_privacy(self):
        """ Wait until CAPTCHA and privacy popups are handled by the user. """
        print("Waiting for CAPTCHA and privacy settings to be solved by the user...")
        
        while True:
            try:
                # Check if CAPTCHA is still present
                self.driver.find_element(By.XPATH, '//*[@id="captcha"]')
                time.sleep(2)
            except:
                break

        while True:
            try:
                # Wait for the privacy banner to disappear (cookies consent)
                self.driver.find_element(By.XPATH, '//*[@id="L2AGLb"]')  # Cookies banner "Accept" button
                time.sleep(2)
            except:
                break
        
        print("CAPTCHA and privacy settings solved, ready for querying!")

    def extract_results(self, query):
        """ Extract search results for the query. """
        try:
            # Wait for search box to be visible
            search_box = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.ID, "APjFqb"))
            )
            
            # Send the query to the search box
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results to load
            time.sleep(3)
            
            # Extract the search result links
            results = self.driver.find_elements(By.XPATH, '//h3//a')
            extracted_results = [(result.text, result.get_attribute("href")) for result in results[:5]]
            
            return extracted_results

        except Exception as e:
            print(f"An error occurred while extracting results: {e}")
            return []

    def handle_queries(self, query_list):
        """ Handle multiple queries and extract results. """
        for query in query_list:
            print(f"Processing query: {query}")
            
            # Check if Google is open and if CAPTCHA/privacy needs to be solved
            if self.check_if_google_open():
                self.wait_for_captcha_and_privacy()
            
            # Extract results
            results = self.extract_results(query)
            
            if results:
                print(f"Results for '{query}':")
                for title, url in results:
                    print(f"- {title}: {url}")
            else:
                print(f"No results found for '{query}'")

    def close_driver(self):
        """ Close the driver. """
        self.driver.quit()


# Example usage

# Initialize BrowserAutomation
automation = BrowserAutomation(debugging_port=9222)

# List of queries to search for
queries = [
    "OpenAI",
    "Selenium Python",
    "GPT-4",
    "Artificial Intelligence"
]

# Handle multiple queries
automation.handle_queries(queries)

# Close the driver when done
automation.close_driver()
