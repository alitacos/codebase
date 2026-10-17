from playwright.async_api import Browser, TimeoutError as PlaywrightTimeoutError
import asyncio


async def capture_pinterest_reset_request(browser: Browser, email: str, password: str | None = None) -> dict:
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

    """async def check_ui_errors():
        selectors = [
            '[role="alert"]',
            "#password-error",
            "#email-error",
        ]

        while True:
            for selector in selectors:
                locator = page.locator(selector)
                if await locator.is_visible():
                    text = await locator.inner_text()
                    raise Exception(f"Pinterest UI error: {text}")

            await page.wait_for_timeout(100)"""
    async def check_ui_errors():
        selectors = [
            '[role="alert"]',
            "#password-error",
            "#email-error",
        ]
    
        while True:
            for selector in selectors:
                locator = page.locator(selector)
    
                if await locator.is_visible():
                    text = await locator.inner_text()
    
                    captured["ui_error"] = text
                    return
    
            await page.wait_for_timeout(100)
    error_task = asyncio.create_task(check_ui_errors())

    try:
        # Load page
        await page.goto(
            "https://de.pinterest.com/",
            wait_until="domcontentloaded"
        )

        # Try cookie decline whenever it appears
        cookie_decline = page.locator('button:has-text("Alle ablehnen")')

        try:
            await cookie_decline.wait_for(
                state="visible",
                timeout=5000
            )
            await cookie_decline.click(force=True)
        except PlaywrightTimeoutError:
            pass

        login_modal = page.locator('[data-test-id="login-modal-default"]')

        # If login modal is not already there, open it immediately
        if not await login_modal.is_visible():
            login_button = page.locator(
                '[data-test-id="simple-login-button"]'
            )

            await login_button.wait_for(
                state="visible",
                timeout=15000
            )

            await login_button.click(force=True)

        # Wait until login fields exist
        await login_modal.wait_for(
            state="visible",
            timeout=15000
        )

        email_input = page.locator(
            '[data-test-id="emailInputField"]'
        )

        password_input = page.locator(
            '[data-test-id="passwordInputField"]'
        )

        await email_input.wait_for(state="visible")
        await password_input.wait_for(state="visible")

        await email_input.fill(email)
        await password_input.fill(password)

        # Check captcha before pressing
        captcha = page.locator(
            "iframe[src*='captcha'], [data-captcha], .captcha"
        )

        if await captcha.is_visible():
            raise Exception("Captcha detected")

        submit = page.locator(
            '[data-test-id="registerFormSubmitButton"] button'
        )

        await submit.wait_for(state="visible")

        # Wait until button is actually usable
        while not await submit.is_enabled():
            await page.wait_for_timeout(100)

        await submit.click()

        # Wait for either request capture or error
        try:
            await asyncio.wait_for(
                asyncio.shield(error_task),
                timeout=15
            )
        except asyncio.TimeoutError:
            pass

        captured["url_after_submit"] = page.url
        captured["alerts"] = await page.locator(
            '[role="alert"]'
        ).all_inner_texts()

        captured["password_error"] = await page.locator(
            "#password-error"
        ).all_inner_texts()

        captured["email_error"] = await page.locator(
            "#email-error"
        ).all_inner_texts()

        return captured

    finally:
        error_task.cancel()
        await context.close()