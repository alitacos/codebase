# not working as expected , does not have good structure, logic, ,leads to error ****  it does not do is thescribed to do...
#
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Generate a unique user-data directory name based on the current timestamp
import time
unique_user_data_dir = f"./User_Data_{int(time.time())}"

# Set up Chrome options to use a specific user data directory (for persistence)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={unique_user_data_dir}")  # Use the unique directory

# Initialize the webdriver with options
driver = webdriver.Chrome(options=chrome_options)

# Open Google Search
driver.get("https://www.google.com")

# Wait for the privacy settings (cookies consent) to appear and handle it manually
print("Please solve the CAPTCHA and accept privacy settings manually. The script will continue once solved.")

# Wait for CAPTCHA or cookies/privacy settings to appear
while True:
    try:
        # Check if CAPTCHA or cookies banner is present (XPath might vary depending on what Google shows)
        # Common cookie banner elements (adjust XPath if needed)
        driver.find_element(By.XPATH, '//*[@id="L2AGLb"]')  # "Accept" button for cookies
        time.sleep(2)  # Wait a couple of seconds if it's present
    except:
        # If no cookie banner or CAPTCHA is found, break out of the loop
        print("Privacy settings and CAPTCHA solved, continuing with extraction...")
        break

# Now wait for the search box (textarea) to be available before interacting
search_box = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "APjFqb"))  # Wait for the search box to be clickable
)

# Scroll to the search box (if it's off-screen)
driver.execute_script("arguments[0].scrollIntoView(true);", search_box)

# Wait for CAPTCHA to disappear (manually solved by the user)
while True:
    try:
        # Check if CAPTCHA is still present
        driver.find_element(By.XPATH, '//*[@id="captcha"]')
        time.sleep(2)  # Wait a couple of seconds if CAPTCHA is present
    except:
        # CAPTCHA is not found, exit the loop
        print("CAPTCHA solved, continuing with extraction...")
        break

# Recheck for search box after CAPTCHA is solved
search_box = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "APjFqb"))  # Recheck that the search box is clickable
)

# Ensure that the search box is enabled
assert search_box.is_enabled(), "Search box is not enabled!"

# Use ActionChains to send the keys to the search box
actions = ActionChains(driver)
actions.move_to_element(search_box).click().send_keys("openai").send_keys(Keys.RETURN).perform()

# Wait for the page to load and display results
time.sleep(3)  # Sleep for a few seconds to ensure results load

# Extract the search result links (just an example, modify as per your needs)
results = driver.find_elements(By.XPATH, '//h3//a')  # XPath for search result links

# Print the titles and URLs of the first few search results
for result in results[:5]:  # Adjust the number to fetch more results if needed
    print(result.text, result.get_attribute("href"))

# Close the browser once done
driver.quit()
