def test_browser_stream_visually_if_headless_or_headfull_via_google_check( page:Page=None )->tuple:
    from urllib.parse import urlparse
    
    
    # Navigate to a new site
    await page.goto("https://accounts.google.com")
    query = "anonymous@gmail.com"
    
    # 1. Fill the input field
    # Replace 'input[type="email"]' or 'input[name="query"]' with the actual selector on your page
    await page.fill('input[type="email"], input[type="text"], input', query)
    
    # 2. Press Enter to submit the form
    await page.keyboard.press("Enter")

    title = await page.title()
     
    parsed = urlparse(page.url)
    scheme, netloc, path,query = parsed.scheme, parsed.netloc, parsed.path, parsed.query 
    print(title,url)
    if 'rejected' in path and 'google' in netloc:
        return 'headless'
    elif  'google' in netloc and ('pwd' in path or 'recaptcha' in path):
        return 'headless'
    raise UnknownError(f'unknown status for {page}. current url:{url}, title:{title}')
    #for any other errors raises automatically 