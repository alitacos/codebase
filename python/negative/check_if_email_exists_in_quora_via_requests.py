def check_if_email_exists_in_quora_via_requests(email: str):
    import requests
    url = 'https://de.quora.com/graphql/gql_para_POST'

    # Properly formatted JSON payload for GraphQL query
    payload = {
        "q": "SignupEmailForm_validateEmail_Query",
        "queryName": "SignupEmailForm_validateEmail_Query",
        "variables": {
            "email": email.strip() if email else ""
        },
        "extensions": {
            "hash": "1db80096407be846d5581fe1b42b12fd05e0b40a5d3095ed40a0b4bd28f49fe7"
        }
    }

    # Cookies as a dictionary (parse from your cookie string or build manually)
    cookies = {
        "m-login": "0",
        "m-b": "ZxA8i4zCvtpN8FUhGm7HOg==",
        "m-b_lax": "ZxA8i4zCvtpN8FUhGm7HOg==",
        "m-b_strict": "ZxA8i4zCvtpN8FUhGm7HOg==",
        "m-s": "EjSbjpGzFs3Tl19d3FwDSA==",
        "m-uid": "None",
        # ...add any other necessary cookies here
        "OptanonConsent": "isGpcEnabled=0&datestamp=Tue+Jun+17+2025+23%3A02%3A54+GMT%2B0200+(Mitteleurop%C3%A4ische+Sommerzeit)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=0694fcd2-63be-4712-8165-6c2fa397ce2e&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A0%2CC0003%3A0%2CC0002%3A0%2CC0001%3A1%2CV2STACK42%3A0"
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        # Sometimes you need to include the full cookie header instead of requests.cookies
        # "Cookie": "<paste cookie string here if needed>"
    }

    response = requests.post(url, json=payload, headers=headers, cookies=cookies)

    try:
        return response.json()
    except Exception:
        return response.text

# Example usage:
#result = check_if_email_exists_in_quora_via_requests("example@gmail.com")
#print(result)
