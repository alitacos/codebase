
import asyncio
from playwright.async_api import  Page

def test_browser_stream_visually_if_headless_or_headfull_via_google_check( page:Page=None )->tuple:
    # Navigate to a new site
    await page.goto("https://accounts.google.com")
    query = "anonymous@gmail.com"
    
    # 1. Fill the input field
    # Replace 'input[type="email"]' or 'input[name="query"]' with the actual selector on your page
    await page.fill('input[type="email"], input[type="text"], input', query)
    
    # 2. Press Enter to submit the form
    await page.keyboard.press("Enter")

    title = await page.title()
    url = await page.url()
    return title,url