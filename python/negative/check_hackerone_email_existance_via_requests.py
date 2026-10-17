import requests
from typing import Union, Dict, Any

def _parse_cookie_string(cookie_string: str) -> Dict[str,str]:
    cookies = {}
    for part in cookie_string.split(';'):
        part = part.strip()
        if not part:
            continue
        if '=' in part:
            k, v = part.split('=', 1)
            cookies[k.strip()] = v.strip()
    return cookies

def check_hackerone_email_existance_via_requests(
    email: str,
    cookies: Union[str, Dict[str,str]] = None,
    headers: Dict[str,str] = None,
    timeout: int = 10
) -> Dict[str, Any]:
    """
    Try to create a user on HackerOne to infer email availability.
    Returns a dict with keys:
      - request_ok: bool   (whether the POST was accepted & returned JSON)
      - blocked_by_cloudflare: bool
      - username_taken: bool  (True if username already taken i.e. request 'worked' as you described)
      - email_taken: bool|None (True if email is taken; False if available; None if can't determine)
      - details: original parsed JSON or raw text (for debugging)
    """

    url = "https://hackerone.com/users"

    # Build payload (form fields)
    payload = {
        "user[name]": "Alice",
        "user[username]": "Alice",
        "user[email]": str(email).strip() if email else "",
        "user[password]": "Bong4life8!040408!",
        "user[password_confirmation]": "Bong4life8!040408!"
    }

    # Default headers
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/115.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            # Content-Type not necessary for form-encoded "data=", requests sets it.
            "Referer": "https://hackerone.com/",
        }

    # Normalize cookies
    cookie_dict = None
    if cookies:
        if isinstance(cookies, str):
            cookie_dict = _parse_cookie_string(cookies)
        elif isinstance(cookies, dict):
            cookie_dict = cookies.copy()
        else:
            cookie_dict = {}
    else:
        cookie_dict = {}

    result = {
        "request_ok": False,
        "blocked_by_cloudflare": False,
        "username_taken": False,
        "email_taken": None,
        "details": None,
        "status_code": None
    }

    try:
        # Use data=payload to send application/x-www-form-urlencoded form data
        resp = requests.post(url, data=payload, cookies=cookie_dict, headers=headers, timeout=timeout)
        result["status_code"] = resp.status_code
        text = resp.text

        # If server returned HTML Cloudflare "Just a moment", detect and return
        if "<!DOCTYPE html>" in text and ("Just a moment" in text or "Enable JavaScript and cookies to continue" in text):
            result["blocked_by_cloudflare"] = True
            result["details"] = text
            return result

        # Try parse json
        try:
            js = resp.json()
            result["request_ok"] = True
            result["details"] = js

            # Typical response example:
            # {
            #   "username": ["has already been taken"],
            #   "email": ["has already been taken"],
            #   ...
            # }
            # Some APIs return errors under "errors" or "error"; handle generically.

            # Check username
            username_errs = js.get("username") or js.get("user") and js.get("user").get("username")  # defensive
            if isinstance(username_errs, list):
                joined = " ".join(username_errs).lower()
                result["username_taken"] = "has already been taken" in joined

            # Now decide email availability
            if "email" in js:
                email_errs = js.get("email")
                # email_errs may be list of strings
                if isinstance(email_errs, list):
                    joined = " ".join(email_errs).lower()
                    if "has already been taken" in joined:
                        result["email_taken"] = True
                    else:
                        # some other error present -> not available for signup as-is
                        result["email_taken"] = False
                elif isinstance(email_errs, str):
                    result["email_taken"] = ("has already been taken" in email_errs.lower())
                else:
                    # unknown structure
                    result["email_taken"] = None
            else:
                # If email key does not exist in response JSON, interpret as "available" per your rule
                result["email_taken"] = False

        except ValueError:
            # Not JSON — fallback: attempt to find textual markers in HTML
            result["details"] = text
            low = text.lower()
            if "has already been taken" in low and "username" in low:
                result["username_taken"] = True
                # if email phrase not present assume available
                if "email" in low and "has already been taken" in low:
                    result["email_taken"] = True
                elif "email" not in low:
                    result["email_taken"] = False
            else:
                # cannot determine
                result["email_taken"] = None

        return result

    except requests.RequestException as e:
        result["details"] = f"request_exception: {e}"
        return result
#cookies_str = "somecookie=somevalue; other=thing"
#out = check_hackerone_email_existance_via_requests("anonymous", cookies='')
#print(out)
