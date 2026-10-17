# check if email exists in web.de as account 
# Unfortunately is not working as web de denies in this way the access for some reason
def check_if_email_exists_in_web_de_(email:str=None, firstName:str=None,lastName:str=None,bday:str=None,city:str=None,countryCode:str=None,initialRequestedEmailAddress:str=None ):#Failed to fetch configuration #Response: {"type":"urn:problem:neo:access-denied","status":403,"title":"Access 
    import requests
    from bs4 import BeautifulSoup
    import json
    import uuid
    session = requests.Session()
    
    url = "https://registrierung.web.de/"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://web.de/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    
    # Step 1: Initial GET
    response = session.get(url, headers=headers, timeout=10)
    print("Initial GET status:", response.status_code)
    print("Cookies after initial GET:", session.cookies.get_dict())
    
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", {"id": "application-config", "type": "application/json"})
    if not script_tag:
        print("No application-config script tag found")
        return
    
    data = json.loads(script_tag.string)
    accessToken = data.get('accessToken', '')
    if not accessToken:
        print("No accessToken found in config")
        return
    
    print("Access Token:", accessToken)
    
    # Step 2: GET /account/configuration to validate session
    headers_config = {
        "accept": "application/vnd.ui.mam.configuration-v1+json",
        "authorization": f"Bearer {accessToken}",
        "content-type": "application/vnd.ui.mam.configuration-v1+json",
        "referer": url,
        "user-agent": headers["user-agent"],
        "x-ccguid": str(uuid.uuid4()),
        "x-request-id": str(uuid.uuid4()),
        "x-ui-app": "@mamdev/umreg.registration-app2/8.20.0"
    }
    
    config_url = "https://registrierung.web.de/account/configuration"
    resp_config = session.get(config_url, headers=headers_config, timeout=10)
    print("Configuration GET status:", resp_config.status_code)
    if resp_config.status_code != 200:
        print("Failed to fetch configuration")
        print("Response:", resp_config.text)
        return
    
    print("Cookies after configuration GET:", session.cookies.get_dict())
    
    # Step 3: POST email alias availability
    
    headers_post = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {accessToken}",
        "content-type": "application/json",
        "origin": "https://registrierung.web.de",
        "referer": url,
        "user-agent": headers["user-agent"],
        "x-ccguid": str(uuid.uuid4()),
        "x-request-id": str(uuid.uuid4()),
        "x-ui-app": "@mamdev/umreg.registration-app2/8.20.0"
    }
    
    payload = {
        "emailAddress": email.strip() if email else "",
        "firstName": firstName.strip() if firstName else "",
        "lastName": lastName.strip() if lastName else "",
        "birthDate": bday.replace('/', '-') if bday else "",
        "city": city.strip() if city else "",
        "countryCode": countryCode.strip() if countryCode else "DE",
        "initialRequestedEmailAddress": initialRequestedEmailAddress.strip() if initialRequestedEmailAddress else "",
        "suggestionProducts": ["webde"],
        "maxResultCountToProduct": {"webde": "4"},
        "mdhMaxResultCount": "4",
        "requestedEmailAddressProduct": "webde"
    }
    
    response_post = session.post(
        "https://register-suggest.web.de/rest/email-alias/availability",
        json=payload,
        headers=headers_post,
        timeout=10
    )
    
    print("POST status:", response_post.status_code)
    
    try:
        json_response = response_post.json()
        print("Response JSON:", json_response)
    except Exception as e:
        print("Failed to parse JSON:", e)
        print("Response text:", response_post.text)

# Example usage:
#check_if_email_exists_in_web_de_(email='alicia@web.de', firstName='Alice', lastName='Alice', bday='1990-04-04')
