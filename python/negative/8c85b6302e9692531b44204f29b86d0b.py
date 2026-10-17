# works but is prefered using type hints, output hints, exception handling
# is a class method. non reusable
# would not work without the expected imports.  
# would not work without the expected variables. non reusable

from selenium.common.exceptions import WebDriverException
from http.client import RemoteDisconnected
from urllib3.exceptions import ProtocolError

def __getattr__(self, name):
    self._ensure_alive()
    attr = getattr(self._driver, name)
    if callable(attr):

        def wrapper(*args, **kwargs):
            try:
                return attr(*args, **kwargs)
            except (WebDriverException, ProtocolError, RemoteDisconnected, Exception) as e:
                print(f'[SelfHealingDriver] Driver call failed: {e}. Reloading and retrying...')
                self.reload()
                try:
                    return getattr(self._driver, name)(*args, **kwargs)
                except Exception as e2:
                    print(f'[SelfHealingDriver] Retry failed: {e2}')
                    raise
        return wrapper
    else:
        return attr