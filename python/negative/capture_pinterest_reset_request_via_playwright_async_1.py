import json
from playwright.async_api import Page, Browser


async def capture_pinterest_reset_request_via_playwright_async(browser: Browser, email: str) -> dict:
    context = await browser.new_context(locale="de-DE")

    page = await context.new_page()

    captured = {}

    async def request_handler(request):
        if "UserSessionResource/create" in request.url:
            captured.update(
                {
                    "url": request.url,
                    "headers": request.headers,
                    "post": request.post_data,
                }
            )

    page.on("request", request_handler)

    await page.goto(
        "https://de.pinterest.com/",
        wait_until="domcontentloaded",
    )

    await page.wait_for_timeout(2000)

    reject_cookie = page.get_by_role(
        "button",
        name="Alle ablehnen",
    )

    if await reject_cookie.count():
        await reject_cookie.first.click()

    login_button = page.get_by_test_id(
        "login-button",
    )

    login_modal = page.get_by_test_id(
        "login-modal-default",
    )

    if not await login_modal.count():
        if await login_button.count():
            await login_button.click()

    await login_modal.wait_for(
        state="visible",
        timeout=10000,
    )

    email_input = page.locator(
        'input[name="id"]'
    )

    await email_input.fill(email)

    reset_link = page.get_by_test_id(
        "password-reset-button",
    )

    if await reset_link.count():
        await reset_link.click()

    await page.wait_for_timeout(5000)

    return captured