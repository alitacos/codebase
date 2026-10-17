# not working as expected , does not have good structure, logic, ,leads to error ****from selenium import webdriver. it does not do is thescribed to do...
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options to use a specific user data directory (for persistence)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=./User_Data")  # Specify the path to your user data directory

# Initialize the webdriver with options
driver = webdriver.Chrome(options=chrome_options)

# Open Google Search
driver.get("https://www.google.com")

# Wait for the search box (textarea) to be available before interacting
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "APjFqb"))  # Now locating the <textarea> element
)

# Try to access the search box directly by its new ID
search_box = driver.find_element(By.ID, "APjFqb")

# Wait for CAPTCHA or privacy settings pop-up to appear and handle manually
print("Please solve the CAPTCHA and accept privacy settings manually. The script will continue once solved.")

# Wait for CAPTCHA to disappear (manually solved by the user)
while True:
    try:
        # Check if CAPTCHA is still present (could be using different XPaths based on Google)
        driver.find_element(By.XPATH, '//*[@id="captcha"]')
        time.sleep(2)  # Wait a couple of seconds if CAPTCHA is present
    except:
        # CAPTCHA is not found, exit the loop
        print("CAPTCHA solved, continuing with extraction...")
        break

# Recheck for search box after CAPTCHA is solved
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "APjFqb"))  # Recheck that the search box is still available
)

# Enter the search query and submit (equivalent to pressing Enter)
search_box.send_keys("openai")
search_box.send_keys(Keys.RETURN)

# Wait for the page to load and display results
time.sleep(3)  # Sleep for a few seconds to ensure results load

# Extract the search result links (just an example, modify as per your needs)
results = driver.find_elements(By.XPATH, '//h3//a')  # XPath for search result links

# Print the titles and URLs of the first few search results
for result in results[:5]:  # Adjust the number to fetch more results if needed
    print(result.text, result.get_attribute("href"))

# Close the browser once done
driver.quit()
