from playwright.sync_api import sync_playwright
import json


def capture_pinterest_reset_request_via_playwright(email):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        context = browser.new_context(
            locale="de-DE",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/148 Safari/537.36"
            )
        )

        page = context.new_page()

        captured = {}

        def handler(request):
            if "UserSessionResource/create" in request.url:
                captured["url"] = request.url
                captured["headers"] = request.headers
                captured["post"] = request.post_data

        page.on("request", handler)

        page.goto(
            "https://de.pinterest.com/password/reset/",
            wait_until="networkidle"
        )

        # adjust selector if Pinterest changes it
        page.fill(
            'input[name="id"]',
            email
        )

        page.wait_for_timeout(5000)

        print(json.dumps(
            captured,
            indent=2
        ))

        browser.close()

        return captured
