from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def set_web_driver(
    browser: str = "chrome",       # 'chrome', 'firefox', 'edge'
    version: int | None = None,    # Driver version (optional)
    headless: bool = False,
    sandbox: bool = True,
    shm: bool = True,
    gpu: bool = True,
    automation_controlled: bool = True,
    exclude_switches: bool = True,
    use_automation_extension: bool = False,
    user_data_dir: str | None = None,
    window_size: tuple[int,int] = (1920,1080),
    incognito: bool = False,
    additional_args: list[str] | None = None
) -> webdriver.Remote | None:
    """
    Factory to create a Selenium WebDriver for Chrome, Firefox, or Edge with flexible options.

    Returns:
        webdriver.Chrome/Firefox/Edge instance, or None if failed.
    """
    try:
        browser = browser.lower()
        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            if not sandbox:
                options.add_argument("--no-sandbox")
            if not shm:
                options.add_argument("--disable-dev-shm-usage")
            if not gpu:
                options.add_argument("--disable-gpu")
            if automation_controlled:
                options.add_argument("--disable-blink-features=AutomationControlled")
            if exclude_switches:
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", use_automation_extension)
            if user_data_dir:
                options.add_argument(f"--user-data-dir={user_data_dir}")
            if window_size:
                options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
            if incognito:
                options.add_argument("--incognito")
            if additional_args:
                for arg in additional_args:
                    options.add_argument(arg)
            
            service = ChromeService(ChromeDriverManager(version=str(version) if version else None).install())
            return webdriver.Chrome(service=service, options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            if window_size:
                options.add_argument(f"--width={window_size[0]}")
                options.add_argument(f"--height={window_size[1]}")
            service = FirefoxService(GeckoDriverManager(version=str(version) if version else None).install())
            return webdriver.Firefox(service=service, options=options)

        elif browser == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            if window_size:
                options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
            service = EdgeService(EdgeChromiumDriverManager(version=str(version) if version else None).install())
            return webdriver.Edge(service=service, options=options)

        else:
            print(f"Browser '{browser}' is not supported.")
            return None

    except Exception as e:
        print(f"Failed to create WebDriver: {e}")
        return None