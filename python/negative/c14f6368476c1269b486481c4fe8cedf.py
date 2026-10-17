from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  

def set_a_simple_chrome_driver_via_selenium(
    browser: str = 'chrome',
    version: int = 146,
    sandbox: bool = False,
    headless: bool = False,
    shm: bool = True,
    gpu: bool = False,
    AutomationControlled: bool = False,
    excludeSwitches: bool = True,
    useAutomationExtension: bool = False,
    user_data_dir = None,
    window_size = "1920,1080",
    incognito: bool = False
) -> webdriver.Chrome | None:
    """
    Create and return a simple Chrome WebDriver with customizable options.

    Args:
        browser (str): The browser type to use (Defaults to 'chrome')
        version (int): ChromeDriver version to use (Defaults to 146)
        sandbox (bool): Disable sandbox mode if False (Defaults to False)
        headless (bool): Run browser in headless mode if True (Defaults to False)
        shm (bool): Use /dev/shm for shared memory (Defaults to True)
        gpu (bool): Enable GPU acceleration if True (Defaults to False)
        AutomationControlled (bool): Hide automation control flags if False (Defaults to False)
        excludeSwitches (bool): Exclude 'enable-automation' switch if True (Defaults to True)
        useAutomationExtension (bool): Disable automation extension if False (Defaults to False)
        user_data_dir (Any): Path to Chrome user data directory (Defaults to None)
        window_size (Any): Set browser window size (Defaults to '1920,1080')
        incognito (Any): Launch browser in incognito mode if True (Defaults to False)

    Returns:
        webdriver.Chrome | None: A Chrome WebDriver instance if successful, else None

    Example usage:
        >>> result = set_a_simple_chrome_driver_via_selenium(
        ...     browser='chrome', version=146, sandbox=False, headless=True,
        ...     shm=True, gpu=False, AutomationControlled=False,
        ...     excludeSwitches=True, useAutomationExtension=False,
        ...     user_data_dir='/path/to/profile', window_size='1920,1080', incognito=True
        ... )
    """
    try:
        options = Options()  # Initialize Chrome options

        # Apply various Chrome options based on arguments
        if headless:
            options.add_argument("--headless")  # Run Chrome without GUI
        if not sandbox:
            options.add_argument("--no-sandbox")  # Disable sandbox for containerized environments
        if not shm:
            options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues in Docker
        if not gpu:
            options.add_argument("--disable-gpu")  # Disable GPU acceleration
        if not AutomationControlled:
            options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation
        if incognito:
            options.add_argument("--incognito")  # Open in incognito mode
        if user_data_dir:
            options.add_argument(f"--user-data-dir={user_data_dir}")  # Specify custom user data
        if window_size:
            options.add_argument(f"--window-size={window_size}")  # Set browser window size
        if excludeSwitches:
            options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Hide automation banner
        options.add_experimental_option("useAutomationExtension", useAutomationExtension)  # Disable extension

        # Return Chrome WebDriver if browser is Chrome
        if browser and browser.lower() in ['chrome', 'google', 'chromium', 'google-chrome', 'google chrome']:
            if version:
                # Install specific ChromeDriver version
                return webdriver.Chrome(ChromeDriverManager(version=str(version)).install(), options=options)
            else:
                return webdriver.Chrome(options=options)
    except Exception:
        # Return None if driver creation fails
        return None