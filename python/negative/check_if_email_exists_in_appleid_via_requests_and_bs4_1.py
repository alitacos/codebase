def check_if_email_exists_in_appleid_via_requests_and_bs4(email: str = None, cookies: dict = {}, headers: dict = {}, payload: dict = {}):
    url = 'https://appleid.apple.com/account/validation/appleid'

    # Payload
    payload = {
        "emailAddress": email if email else ""
    }

    # REQUIRED: Replace these with fresh headers from browser
 
    try:
        response = requests.post(url,   json=payload, timeout=10)
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
        self.error = call['error']
        self.status_code = call['status_code']
        self.message = call['message']
        self.available = call['available']

    def __repr__(self):
        return f"<AppleIDChecker email='{self.email}' available={self.available}>"

#example usage
#test1 = check_if_email_exists_in_appleid_via_requests_and_bs4(email='alitakos90@gmail.com')  # Should return available = 1# [DEBUG] Status: 503\nExpecting value: line 1 column 1 (char 0)\ 
#test1 = AppleIDChecker(email='alitakos90@gmail.com')  # Should return available = 1# [DEBUG] Status: 503\nExpecting value: line 1 column 1 (char 0)\ 
