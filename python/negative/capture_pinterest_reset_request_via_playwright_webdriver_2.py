async def capture_pinterest_reset_request_via_playwright_webdriver(browser, email):
    context = await browser.new_context(locale="de-DE")
    page = await context.new_page()
    captured = {}

    async def capture(request):
        if "UserSessionResource/create" in request.url:
            captured.update(url=request.url, headers=request.headers, post=request.post_data)

    async def click_text(text):
        locator = page.get_by_text(text, exact=True)
        if await locator.count():
            await locator.first.click(force=True)
            return True
        return False

    page.on("request", capture)

    await page.goto("https://de.pinterest.com/", wait_until="domcontentloaded")

    await page.wait_for_timeout(3000)

    await click_text("Alle ablehnen")

    await page.wait_for_timeout(2000)

    if not await page.locator('[data-test-id="login-modal-default"]').count():
        login = page.locator('[data-test-id="login-button"]')

        if await login.count():
            await login.click(force=True)

    await page.locator('[data-test-id="login-modal-default"]').wait_for()

    await page.locator('[data-test-id="emailInputField"]').fill(email)

    await page.wait_for_timeout(15000)

    await context.close()

    return captured