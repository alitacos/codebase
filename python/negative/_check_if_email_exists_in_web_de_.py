import requests
from bs4 import BeautifulSoup
import json
#returns #Cookies: {'AB_COOKIE': 'B'} Config status: 403 {"type":"urn:problem:neo:access-denied","status":403,"title":"Access Denied","
session = requests.Session()

# Step 1: initial GET to get token and cookies
response = session.get("https://registrierung.web.de/", headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
})

soup = BeautifulSoup(response.text, "html.parser")
script_tag = soup.find("script", {"id": "application-config", "type": "application/json"})
if not script_tag:
    print("No config found")
    exit()

data = json.loads(script_tag.string)
access_token = data.get('accessToken')

print("Access token:", access_token)
print("Cookies:", session.cookies.get_dict())

# Step 2: call configuration endpoint
headers_config = {
    "accept": "application/vnd.ui.mam.configuration-v1+json",
    "authorization": f"Bearer {access_token}",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "referer": "https://registrierung.web.de/",
    "x-ui-app": "@mamdev/umreg.registration-app2/8.20.0"
}

config_resp = session.get("https://registrierung.web.de/account/configuration", headers=headers_config)
print("Config status:", config_resp.status_code)
print(config_resp.text)
