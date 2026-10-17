import asyncio
from playwright.async_api import Page 
async def check_if_username_input_exists_in_facebook_playwright_Page(page:Page=None,  selector:str="input[name='accountIdentifier']" ,alt_selector:str="input[type='text'][class='SignInForm_input__CtA7_']", timeout:int=2000 )->bool:
#async def check_if_username_input_exists(page:Page=None,query:str='' , selector:str="input[name='accountIdentifier']"  timeout:int=2000 )->bool:
    try:
        inputElement = page.locator(selector.strip()).first or page.locator(alt_selector.strip()).first 
        if inputElement.count():
            #await inputElement.fill(query.strip())
            #await inputElement.press("Enter")
            return  True
        return False
    except Exception as e:
        #print(e)
        return False