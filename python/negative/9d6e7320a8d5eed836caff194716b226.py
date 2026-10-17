# works but is prefered using type hints, output hints, exception handling
# is a class method. non reusable
# would not work without the expected imports.  
# would not work without the expected variables. non reusable
def _is_alive(self):
    try:
        _ = self._driver.title
        return True
    except Exception:
        return False