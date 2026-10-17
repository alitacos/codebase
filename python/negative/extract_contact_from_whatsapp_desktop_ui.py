
import undetected_chromedriver  
from selenium import webdriver
    
def extract_contact_from_whatsapp_desktop_ui(driver: driver:webdriver.Chrome | undetected_chromedriver.Chrome = None,  number:str='')->dict:
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import time
    def enter_text_in_field_in_contacts_searchbar(driver: webdriver.Chrome | uc.Chrome = None, phone_number:str='')->bool:
         
        def press_clear_button(driver: webdriver.Chrome | uc.Chrome = None)->bool:
            try:
                # Locate the clear button
                clear_button = driver.find_element(By.XPATH, '//*[@aria-label="Suchvorgang abbrechen"] | //*[@aria-label="Cancel search"]')
                
                # Use JavaScript to click the clear button directly
                driver.execute_script("arguments[0].click();", clear_button)
                #print("Clear button clicked successfully.")
                return True
            except Exception as e:
                #print(f"Error with clear button: {e}")
                return False
    
        try:
            # Press the clear button if possible
            press_clear_button(driver)
            
            # Step 1: Locate the input field
            input_field = driver.find_element(By.CSS_SELECTOR, "div.x1hx0egp.x6ikm8r.x1odjw0f.x6prxxf.x1k6rcq7.x1whj5v[contenteditable='true']")
            
            # Step 2: Click the input field to focus on it
            input_field.click()
            #print("Input field clicked and focused.")
            
            # Step 3: Clear any pre-existing text
            input_field.clear()
            #print("Cleared existing text in the input field.")
            
            # Step 4: Enter the phone number
            input_field.send_keys(phone_number)
            #print(f"Entered phone number: {phone_number}")
            
            return True
        
        except Exception as e:
            # Catch all errors but do not raise them
            #print(f"Error entering phone number: {e}")
            return False
    #enter_text_in_field_in_contacts_searchbar(driver, '+491d680627892')
    # Function to wait for the text "Es wird außerhalb deiner Kontakte gesucht" to disappear
    def wait_for_text_to_disappear(driver: webdriver.Chrome | uc.Chrome = None, timeout:int=30, check_interval:int=1)->bool:
        start_time = time.time()
        while True:
            # Get page source and parse with BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Check if the text exists in the page
            if not soup.find(string="Es wird außerhalb deiner Kontakte gesucht"):
                #print("Text 'Es wird außerhalb deiner Kontakte gesucht' is no longer visible.")
                return True
            
            # Check timeout
            if time.time() - start_time > timeout:
                #print("Timed out waiting for text to disappear.")
                return False
            
            # Wait for a while before checking again
            time.sleep(check_interval)

    # Wait for the text to disappear before proceeding
    if not wait_for_text_to_disappear(driver):
        return {'international': number, 'valid': False, 'img': '', 'info': ''}

    # Define XPaths
    element_1_xpath = f"//span[@title='{number}' and contains(@class, 'x1iyjqo2')]"
    element_2_xpath = "//div[@data-tab='4' and contains(@class, '_ak72')]"
    element_3_xpath = "//div[@tabindex='-1']//div[contains(@class, '_ak72')]//img[@src and contains(@class, 'x1n2onr6')]"

    # Function to check for the contact element
    def check_element_exists(driver, number: str = ''):
        try:
            driver.find_element(By.XPATH, element_3_xpath)
            return 3
        except:
            pass

        try:
            driver.find_element(By.XPATH, element_2_xpath)
            return 2
        except:
            pass

        try:
            driver.find_element(By.XPATH, element_1_xpath)
            return 1
        except:
            pass

        return 0

    out = {'international': '', 'valid': False, 'img': '', 'info': ''}

    # Wait until the contact is located
    element_type = check_element_exists(driver, number)

    # Extract information based on the element type found
    if element_type == 3:
        try:
            img_element = driver.find_element(By.XPATH, element_3_xpath)
            out['img'] = img_element.get_attribute("src")
            num_el = driver.find_element(By.XPATH, f"//span[@title='{number}' and contains(@class, 'x1iyjqo2')]")
            out['international'] = "".join(num_el.get_attribute("title").split())
            out['valid'] = True
        except Exception as e:
            #print(f"Error extracting image or contact details: {e}")
            out['valid'] = False

    elif element_type == 2:
        try:
            div = driver.find_element(By.XPATH, element_2_xpath)
            num_el = div.find_element(By.XPATH, ".//span[contains(@class, 'x6ikm8r')]")
            out['international'] = "".join(num_el.get_attribute("title").split())
            out['valid'] = True
        except Exception as e:
            #print(f"Error extracting contact from element type 2: {e}")
            out['valid'] = False
    elif element_type == 1:
        try:
            element_1 = driver.find_element(By.XPATH, f"//span[@title='{number}' and contains(@class, 'x1iyjqo2')]")
            out['international'] = "".join(element_1.text.split())  # .text to get visible text
            out['valid'] = True
        except Exception as e:
            print(f"Error extracting contact from element type 1: {e}")
            out['valid'] = False
    # Extract additional info if available
    try:
        info_element = driver.find_element(By.XPATH, "//div[contains(@class, '_ak8j')]//span[@data-testid='selectable-text']")
        out['info'] = info_element.text.strip() if info_element else ''
    except Exception as e:
        #print(f"Error extracting additional info: {e}")
        out['info'] = ''

    # Return the result
    if out.get('international', '') == number:
        return out
    out['valid'] = False
    return out

# Example usage:
# driver = # Your Selenium WebDriver instance here
# number = '+4917663310141'  # Example phone number
#result = extract_contact(driver, number)
#print(result)