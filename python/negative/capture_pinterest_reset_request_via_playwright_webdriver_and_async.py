from playwright.async_api import async_playwright


async def capture_pinterest_reset_request_via_playwright_webdriver_and_async(email, chrome_path="/usr/bin/google-chrome", timeout=15000):
    captured = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, executable_path=chrome_path)

        context = await browser.new_context(locale="de-DE", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36")

        page = await context.new_page()

        async def handler(request):
            if "UserSessionResource/create" in request.url:
                captured["url"] = request.url
                captured["headers"] = request.headers
                captured["post"] = request.post_data

        page.on("request", handler)

        await page.goto("https://de.pinterest.com/password/reset/", wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)

        for selector in ["input[name='id']", "input[type='email']", "input[placeholder*='Email']", "input[placeholder*='email']"]:
            field = page.locator(selector)

            if await field.count():
                await field.first.fill(email)
                break
        else:
            raise RuntimeError("Pinterest email input not found")

        await page.wait_for_timeout(timeout)

        await browser.close()

    return captured