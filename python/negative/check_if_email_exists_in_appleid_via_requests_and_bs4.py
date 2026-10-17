def check_if_email_exists_in_appleid_via_requests_and_bs4(email: str = None, cookies: dict = {}, headers: dict = {}, payload: dict = {}):
    import requests
    from bs4 import BeautifulSoup

    url = 'https://appleid.apple.com/account/validation/appleid'

    # Payload
    payload = {
        "emailAddress": email if email else ""
    }

    # REQUIRED: Replace these with fresh headers from browser
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": "https://appleid.apple.com",
        "referer": "https://appleid.apple.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "x-apple-i-fd-client-info": '{"U":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36","L":"de-DE","Z":"GMT+02:00","V":"1.1"}',
        "x-apple-i-timezone": "Europe/Berlin",
        "x-apple-id-session-id": "kJEOTM5OUVFMUI4NTgyOEM5Njc0MDIwQ0Y4MkEzMEE2QjFBOUMxMzQ4N0FDMzk2REVEMjBGRjNCRTc2N0Y5QzgxOTI4NzkxNEE2RDMyQjE1M0UyRjY1QTIxMTY3RDgzNENBQzg3NDdBMjNDNkZFQTJCRjQ5QjYwRTYxM0I4MDA0RUE1QjBCNTlCNjkwQUMwMDE1MkZBRjA4NjFCMEIxNDU4RUExOUEzMUVFQkZFQjA0RDg1RjdGQzMwMzNGOUMxNzUwMkU3RDU4MzhFNEUwRkJDQjU1RkUxRTQ5RUU2MTgxQTlGQjg2N0ZBODBFRTExQ3w0AAABmZwzoY",
        "x-apple-request-context": "account",
        "x-apple-widget-key": "af1139274f266b22b68c2a3e7ad932cb3c0bbe854e13a79af78dcc73136882c",
        "scnt": "YOUR_VALID_SCNT_HERE"
    }

    cookies = {
    "dslang": "DE-DE",
    "site": "DEU",
    "geo": "DE",
    "idclient": "web",
    "aidsp": "BD9399EE1B85828C9674020CF82A30A6B1A9C13487AC396DED20FF3BE767F9C819287914A6D32B153E2F65A21167D834CAC8747A23C6FEA2BF49B60E613B8004EA5B0B59B690AC00152FAF0861B0B1458EA19A31EEBFEB04D85F7FC3033F9C17502E7D5838E4E0FBCB55FE1E49EE6181A9FB867FA80EE11C",
    "adsv": "e5iEo8lX5g",
    "aid": "6E5C99E1864EFF7BC77FF2B4E680B2E0"
}

    try:
        response = requests.post(url, cookies=cookies, headers=headers, json=payload, timeout=10)
        print(f"[DEBUG] Status: {response.status_code}")

        content_type = response.headers.get("Content-Type", "")
        try:
            dictionary = response.json()
            print(f"[DEBUG] JSON: {dictionary}")
        except Exception as e3:
            print(e3)
        if "application/json" not in content_type:
            return {
                "error": "Non-JSON response. Possibly blocked or invalid session.",
                "status_code": response.status_code,
                "message": response.text[:500],
                "available": None
            }
        used = dictionary.get("used")
        valid = dictionary.get("valid")

        if used is True:
            return {
                "available": 0,
                "error": None if valid else "invalid email",
                "status_code": response.status_code,
                "message": dictionary
            }
        elif used is False:
            return {
                "available": 1,
                "error": None if valid else "invalid email",
                "status_code": response.status_code,
                "message": dictionary
            }
        else:
            return {
                "error": "Unknown response from Apple",
                "status_code": response.status_code,
                "message": dictionary,
                "available": None
            }

    except Exception as e:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            msg = soup.find('h1').text if soup.find('h1') else soup.text[:200]
            return {
                "error": str(e),
                "status_code": response.status_code if response else None,
                "message": msg,
                "available": None
            }
        except Exception as inner_e:
            return {
                "error": str(inner_e),
                "status_code": None,
                "message": None,
                "available": None
            }


class AppleIDChecker:
    def __init__(self, email: str = None):
        self.email = email.strip() if email else None
        self.source = 'apple.com'
        call = check_if_email_exists_in_appleid_via_requests_and_bs4(email=self.email)
        print(call)
        self.error = call['error']
        self.status_code = call['status_code']
        self.message = call['message']
        self.available = call['available']

    def __repr__(self):
        return f"<AppleIDChecker email='{self.email}' available={self.available}>"


#example usage
#test1 = AppleIDChecker(email='alitakos90@gmail.com')  # Should return available = 1
#[DEBUG] Status: 503\nExpecting value: line 1 column 1 (char 0)\n{'error': 'Non-JSON response. Possibly blocked or invalid session.', 'status_code': 503, 'message': '<html>\r\n<head><title>503 Service Temporarily Unavailable</title></head>\r\n<body>\r\n<center><h1>503 Service Temporarily Unavailable</h1></center>\r\n<hr><center>Apple</center>\r\n</body>\r\n</html>\r\n<!-- a padding to disable MSIE and Chrome friendly error page -->\r\n<!-- a padding to disable MSIE and Chrome friendly error page -->\r\n<!-- a padding to disable MSIE and Chrome friendly error page -->\r\n<!-- a padding to disable MSIE and Chrome friendly error page -->\r\n<!-- a padding to disable MSIE and Chrome ', 'available': None}
