from playwright.async_api import Browser


async def capture_pinterest_reset_request_via_playwright_async(browser: Browser, email: str) -> dict:
    context = await browser.new_context(locale="de-DE")
    page = await context.new_page()

    captured = {}

    async def handle_request(request):
        if "UserSessionResource/create" in request.url:
            captured["url"] = request.url
            captured["headers"] = request.headers
            captured["post"] = request.post_data

    page.on("request", handle_request)

    await page.goto("https://de.pinterest.com/", wait_until="domcontentloaded")
    await page.wait_for_timeout(3000)

    cookie_decline = page.locator('button:has-text("Alle ablehnen")')

    if await cookie_decline.count():
        await cookie_decline.click(force=True)

    login_modal = page.locator('[data-test-id="login-modal-default"]')

    if not await login_modal.count():
        login_button = page.locator('[data-test-id="simple-login-button"]')
        await login_button.wait_for(state="attached", timeout=15000)
        await login_button.click(force=True)

    await login_modal.wait_for(state="visible", timeout=15000)

    email_input = page.locator('input[name="id"]')
    await email_input.wait_for(state="visible", timeout=10000)
    await email_input.fill(email)

    await page.get_by_test_id("password-reset-button").click()

    await page.wait_for_timeout(5000)

    await context.close()

    return captured