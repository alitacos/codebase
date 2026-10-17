def make_pinterest_request_and_check_email_availability(username_or_email, password=None, verbose=True):
    import json
    import time
    import requests
    s = requests.Session()

    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/148.0.0.0 Safari/537.36"
    )

    # 1. Open the page first to obtain fresh cookies
    r = s.get(
        "https://de.pinterest.com/password/reset/",
        headers={
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml",
        },
    )

    csrf = s.cookies.get("csrftoken")

    if verbose:
        print("Initial cookies:")
        print(s.cookies.get_dict())
        print("CSRF:", csrf)

    # 2. Build request body
    payload = {
        "options": {
            "username_or_email": username_or_email,
            "password": password or username_or_email,
            "get_user": True,
            "app_type_from_client": 5,
            "visited_pages_before_login": json.dumps([
                {
                    "path": "/password/reset/",
                    "pageType": "",
                    "ts": int(time.time() * 1000),
                }
            ]),
            "handler": "www/password/reset.js",
            "ui_component": "unauth_header.Login",
        },
        "context": {},
    }

    form = {
        "source_url": "/password/reset/",
        "data": json.dumps(payload),
    }

    # 3. API headers
    headers = {
        "User-Agent": ua,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://de.pinterest.com",
        "Referer": "https://de.pinterest.com/password/reset/",
        "X-Requested-With": "XMLHttpRequest",
        "X-Pinterest-AppState": "active",
        "X-Pinterest-PWS-Handler": "www/password/reset.js",
        "X-Pinterest-Source-Url": "/password/reset/",
        "X-App-Version": "aad8170",
    }

    if csrf:
        headers["X-CSRFToken"] = csrf

    # 4. Send request using the same session
    response = s.post(
        "https://de.pinterest.com/resource/UserSessionResource/create/",
        headers=headers,
        data=form,
    )

    if verbose:
        print("Status:", response.status_code)
        print(response.text)

    return response
