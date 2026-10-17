# works but is prefered using type hints, output hints, exception handling
# is a class method. non reusable
# would not work without the expected imports.  
# would not work without the expected variables. non reusable
def _ensure_alive(self):
    if self._driver is None or not self._is_alive():
        self.reload()