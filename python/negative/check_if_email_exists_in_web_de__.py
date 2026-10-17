import requests
# for some reason is not working. returns JSONDecodeError                           
# Session to keep cookies across requests
session = requests.Session()

# Step 1: GET root page to get access token + cookies
url_root = "https://registrierung.web.de/"
resp_root = session.get(url_root)
resp_root.raise_for_status()

# The response looks like JSON with accessToken inside, so parse it
data = resp_root.json()

access_token = data.get("accessToken")
if not access_token:
    raise Exception("No access token found in initial response")

print("Access token:", access_token)

# Step 2: Use access token to call email alias availability API

url_alias = "https://register-suggest.web.de/rest/email-alias/availability"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://registrierung.web.de",
    "Referer": "https://registrierung.web.de/",
    # Add User-Agent and any other required headers here
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

payload = {
  "emailAddress": "aa.aa@web.de",
  "firstName": "Aa",
  "lastName": "Aa",
  "birthDate": "1990-04-04",
  "city": "",
  "countryCode": "DE",
  "initialRequestedEmailAddress": "",
  "suggestionProducts": ["webde"],
  "maxResultCountToProduct": {"webde": "4"},
  "mdhMaxResultCount": "4",
  "requestedEmailAddressProduct": "webde"
}

resp_alias = session.post(url_alias, json=payload, headers=headers)
resp_alias.raise_for_status()

print(resp_alias.json())
