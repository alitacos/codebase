# requires error and exeption handling. Even after better code, the process returns javascript, so would not load
def check_if_email_exists_in_paypal_via_requests_and_bs4(email: str = None, cookies: dict = None, headers: dict = None, payload: dict = None):
    import requests
    from bs4 import BeautifulSoup
    url = 'https://www.paypal.com/welcome/rest/v1/emailExists'

    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Content-Type": "application/json"
        }

    if cookies is None:
        cookies = {
            # Add minimal cookies here if required — may not be necessary for initial test
        }

    if payload is None:
        payload = {
            "email": str(email).strip() if email else ""
        }

    try:
        response = requests.post(url, headers=headers, cookies=cookies, json=payload)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"[Error] Request failed: {e}")
        return None


# === Usage Example ===
#res = check_if_email_exists_in_paypal(email='anon@gmail.com')

#if res:
#    try:
#        print(res.json())
#    except Exception:
#        soup = BeautifulSoup(res.content, 'html.parser')
#        body_text = soup.find('body').text.strip() if soup.find('body') else "No body content"
#        print("[HTML Fallback Response]:")
#        print(body_text)
