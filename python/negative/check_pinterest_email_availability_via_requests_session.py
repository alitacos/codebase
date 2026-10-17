def check_pinterest_email_availability_via_requests_session(email: str, password: str = "", verbose=False):
    import requests
    import json
    import time

    s = requests.Session()

    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/148.0.0.0 Safari/537.36"
    )

    # Step 1: create browser-like session
    page = s.get(
        "https://de.pinterest.com/password/reset/",
        headers={
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
        },
    )

    if verbose:
        print("GET:", page.status_code)
        print("cookies:", s.cookies.get_dict())


    csrf = s.cookies.get("csrftoken")

    if not csrf:
        print("No CSRF cookie")
        return False


    # Step 2: request payload
    payload = {
        "options": {
            "username_or_email": email,
            "password": password or email,
            "get_user": True,
            "app_type_from_client": 5,

            "visited_pages_before_login": json.dumps([
                {
                    "path": "/password/reset/",
                    "pageType": "",
                    "ts": int(time.time()*1000)
                }
            ]),

            "handler": "www/password/reset.js",
            "ui_component": "unauth_header.Login",
        },
        "context": {}
    }


    headers = {
        "User-Agent": ua,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded",

        "Origin": "https://de.pinterest.com",
        "Referer": "https://de.pinterest.com/password/reset/",

        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrf,

        "X-Pinterest-AppState": "active",
        "X-Pinterest-PWS-Handler": "www/password/reset.js",
        "X-Pinterest-Source-Url": "/password/reset/",

        "X-App-Version": "aad8170",
    }
    headers = {
    "User-Agent": ua,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded",

    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",

    "Origin": "https://de.pinterest.com",
    "Referer": "https://de.pinterest.com/",

    "X-Requested-With": "XMLHttpRequest",
    "X-CSRFToken": csrf,

    "X-Pinterest-AppState": "active",
    "X-Pinterest-PWS-Handler": "www/password/reset.js",
    "X-Pinterest-Source-Url": "/password/reset/",
    "X-App-Version": "aad8170",

    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

    r = s.post(
        "https://de.pinterest.com/resource/UserSessionResource/create/",
        headers=headers,
        data={
            "source_url": "/password/reset/",
            "data": json.dumps(payload)
        }
    )


    if verbose:
        print(r.status_code)
        print(r.text[:1000])


    try:
        data = r.json()

        error = (
            data
            .get("resource_response", {})
            .get("error")
        )


        if error:

            code = error.get("api_error_code")

            # Account missing
            if code == 79:
                return {
                    "email": email,
                    "exists": False,
                    "reason": error["message"]
                }


            return {
                "email": email,
                "exists": None,
                "error": error
            }


        # successful response normally means account exists
        return {
            "email": email,
            "exists": True,
            "response": data
        }


    except Exception:
        return False