import asyncio
import json
from playwright.async_api import async_playwright


async def capture_pinterest_reset_request_via_playwright_and_chrome(email):

    async with async_playwright() as p:

#        browser = await p.chromium.launch(            headless=False)
        browser = await p.chromium.launch(
    headless=False,
    executable_path="/usr/bin/google-chrome",
)
        context = await browser.new_context(
            locale="de-DE",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/148.0.0.0 Safari/537.36"
            )
        )

        page = await context.new_page()

        captured = {}

        async def handler(request):

            if "UserSessionResource/create" in request.url:

                print("\n===== REQUEST FOUND =====")

                captured["url"] = request.url
                captured["headers"] = request.headers
                captured["post"] = request.post_data

                print("\nURL:")
                print(request.url)

                print("\nHEADERS:")
                print(json.dumps(
                    request.headers,
                    indent=2
                ))

                print("\nPOST:")
                print(request.post_data)


        page.on(
            "request",
            handler
        )


        print("Opening Pinterest...")

        await page.goto(
            "https://de.pinterest.com/password/reset/",
            wait_until="domcontentloaded"
        )


        await page.wait_for_timeout(5000)


        # Debug inputs
        inputs = await page.locator("input").count()

        print("\nInputs found:", inputs)

        for i in range(inputs):

            el = page.locator("input").nth(i)

            print(
                i,
                await el.get_attribute("name"),
                await el.get_attribute("placeholder"),
                await el.get_attribute("type")
            )


        # Try common Pinterest email selectors

        selectors = [
            'input[name="id"]',
            'input[type="email"]',
            'input[placeholder*="Email"]',
            'input[placeholder*="email"]',
        ]


        filled = False

        for selector in selectors:

            try:
                loc = page.locator(selector)

                if await loc.count() > 0:

                    await loc.first.fill(email)

                    print(
                        "Filled using:",
                        selector
                    )

                    filled = True
                    break

            except Exception:
                pass


        if not filled:

            print(
                "Could not find email input"
            )

            await page.pause()


        # Give Pinterest JS/challenges time

        print(
            "Waiting for request..."
        )

        await page.wait_for_timeout(
            15000
        )


        print(
            "\nCaptured data:"
        )

        print(
            json.dumps(
                captured,
                indent=2
            )
        )


        await browser.close()

        return captured
