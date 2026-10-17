from playwright.async_api import async_playwright

async def capture_pinterest_reset_request_loading_playwright_driver_and_quit(browser, email):
    context = await browser.new_context(locale="de-DE")
    page = await context.new_page()
    captured = {}

    async def capture(request):
        if "UserSessionResource/create" in request.url:
            captured.update(url=request.url, headers=request.headers, post=request.post_data)

    async def click_if_exists(selector):
        element = page.locator(selector)
        if await element.count():
            await element.first.click()
            await page.wait_for_timeout(1000)
            return True
        return False

    page.on("request", capture)

    await page.goto("https://de.pinterest.com/", wait_until="domcontentloaded")

    await click_if_exists("button:has-text('Alle ablehnen')")

    if not await page.locator('[data-test-id="login-modal-default"]').count():
        await click_if_exists('[data-test-id="login-button"]')

    await page.locator('[data-test-id="login-modal-default"]').wait_for()

    await page.locator('input[name="id"]').fill(email)

    await page.wait_for_timeout(15000)

    await context.close()

    return captured
async with async_playwright() as p:
    browser = await p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=False)

    request = await capture_pinterest_reset_request(browser, "alitakos90@gmail.de")

    print(json.dumps(request, indent=2))

    await browser.close()