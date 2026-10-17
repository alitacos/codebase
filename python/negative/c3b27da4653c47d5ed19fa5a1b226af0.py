# works but is prefered using type hints, output hints, exception handling
# is a class method. non reusable
# would not work without the expected imports.  
# would not work without the expected variables. non reusable
import undetected_chromedriver as uc

def _open_driver(self):
    print('Opening new driver...')
    options = uc.ChromeOptions()
    if self.headless:
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-data-dir=/tmp/uc_profile')
    self._driver = uc.Chrome(options=options)