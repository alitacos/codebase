from playwright.async_api import Browser


async def capture_pinterest_reset_request_via_playwright(browser: Browser, email: str, password: str | None = None) -> dict:
    if password is None:
        password = email

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

    if await cookie_decline.count() and await cookie_decline.is_visible():
        await cookie_decline.click(force=True)
        await page.wait_for_timeout(2000)

    login_modal = page.locator('[data-test-id="login-modal-default"]')

    if not await login_modal.is_visible():
        login_button = page.locator('[data-test-id="simple-login-button"]')
        await login_button.wait_for(state="visible", timeout=15000)
        await login_button.click(force=True)

    await login_modal.wait_for(state="visible", timeout=15000)

    email_input = page.locator('[data-test-id="emailInputField"]')
    password_input = page.locator('[data-test-id="passwordInputField"]')

    await email_input.wait_for(state="visible", timeout=10000)
    await password_input.wait_for(state="visible", timeout=10000)

    await email_input.fill(email)
    await page.wait_for_timeout(1500)

    await password_input.fill(password)
    await page.wait_for_timeout(3000)

    submit = page.locator('[data-test-id="registerFormSubmitButton"] button')

    await submit.wait_for(state="visible", timeout=10000)
    await page.wait_for_timeout(3000)

    await submit.click()

    await page.wait_for_timeout(10000)

    captured["url_after_submit"] = page.url
    captured["alerts"] = await page.locator('[role="alert"]').all_inner_texts()

    captured["password_error"] = await page.locator("#password-error").all_inner_texts()
    captured["email_error"] = await page.locator("#email-error").all_inner_texts()

    await context.close()

    return captured