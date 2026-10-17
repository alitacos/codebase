import json


async def capture_pinterest_reset_request_via_playwright_webdriver(browser, email):
    context = await browser.new_context(locale="de-DE")
    page = await context.new_page()

    captured = {}

    async def capture(request):
        if "UserSessionResource/create" in request.url:
            captured.update({
                "url": request.url,
                "headers": request.headers,
                "post": request.post_data
            })

    page.on("request", capture)

    await page.goto("https://de.pinterest.com/password/reset/", wait_until="domcontentloaded")

    await page.locator('input[name="id"], input[type="email"]').first.fill(email)

    await page.wait_for_timeout(15000)

    await context.close()

    return captured