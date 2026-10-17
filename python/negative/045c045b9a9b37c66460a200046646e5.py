def set_a_chrome_driver_via_seleniumy(service:str='chrome',version:int=146, sandbox: bool = False, headless:bool=False, shm: bool = True, gpu: bool = False,AutomationControlled:bool=False,excludeSwitches:bool=True,useAutomationExtension:bool=False) -> Display | None:
    try:
        options = Options()
        # add some more options## data_dir, type of driver (chrome,firefox, edge) and else
        if headless:
            options.add_argument("--headless")
        if not sandbox:
            options.add_argument("--no-sandbox")
        if not shm:
            options.add_argument("--disable-dev-shm-usage")
        if not gpu:
            options.add_argument("--disable-gpu")
        if not AutomationControlled:
            options.add_argument("--disable-blink-features=AutomationControlled")
        if excludeSwitches:
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", useAutomationExtension)
        if service and service.lower() in  ['chrome','google','chromium','google-chrome','google chrome']:
            return webdriver.Chrome(options=options)#add version version

    except Exception:
        return None
