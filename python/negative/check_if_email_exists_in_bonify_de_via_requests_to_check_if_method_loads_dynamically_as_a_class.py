def check_if_email_exists_in_bonify_de_via_requests_to_check_if_method_loads_dynamically_as_a_class(email: str = '',cookies:dict={},headers:dict={},payload:dict={} ) -> object:
    """
    Check if an email user ID exists in okx registration system.
    OKX has no exposure of the 'email' other users, so None method will work without direct access into the database.
    """
    import requests
    from bs4 import BeautifulSoup
    if not email:
        raise ValueError("Email must be provided")
    
        

    url='https://sso.bonify.de/oauth2/authorize'
    if not payload:
        payload = {"client_id":"c7c95483-c023-4cc6-9e99-9f5aaabcff29",
"code_challenge":"gmv24cTiythCds5da33lYfCwj16yZjeAOC935t8i8zg",
"code_challenge_method":"S256",
"metaData.device.name":"Windows Chrome",
"metaData.device.type":"BROWSER",
"nonce":"",
"redirect_uri":"https://my.bonify.de/callback",
"response_mode":"query",
"response_type":"code",
"scope":"openid profile",
"state":"5b8c3cbe541042ea891e8c61ac60f701",
"tenantId":"d53c5515-7538-45f1-ac0c-4f7021bb2e62",
"timezone":"Europe/Berlin",
"user_code":"",
"step":1,
"registrationState"
"parentEmailRequired":"false",
"user.email" :  str(email).strip() if email else "",
"user.password":"",
"user.data.utmCampaignv":"",
"user.data.utmMediumv":"",
"user.data.utmSource":"",
"user.data.utmContent":"",
"user.data.utmTerm":"",
"user.data.utmConsentCheckbox":"",
"user.data.couponCode":"",
"user.data.anonymousId":"",
"user.data.bonifyContest":""}

    if not headers:
        headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}
# If you need cookies, define them like this:
    if not cookies:
        cookies = {'ak_bmsc': '157FDB9D78EDBA4D4E5E20B7A1FBE30E~000000000000000000000000000000~YAAQyqEkF6ivamCXAQAAnMBrgxzQzDcT953RyWlogJ5nrnKNyEZXRkXbm0EdZC9FvQswg+epYyPsO/0qWL7tNCUm2OOCMUjJquctg2MVSfF2Y9v3St9DrR/Xi/Lyf8cXfmh8bLadt6KAkYU+4VCgBMWeCB45zPNOtE20LxLvmysS7+aRD/l3easL4hZJA5a5avf2JCt35GfvboLO+YaYzjgDIEO4PT7btPkGYiwNa3arYWx0MB57htBDSyvIbx6bpYNo3a03QzBVP7+1K8ndbZxhImSSLawIxiAhK7hse15w1iXTkeATdT/ukTUEOFof8DhX8PiXhbfc7kuobdpLWlpvPEz7tguVmtos0fCafrQaS64qb9ECCYGlW8ZGEZq4T526PlFKN0wXLGw+UoOauZWSZ8cOZzM74a8Er5vC2RCJNZn22iVwBKEFDCLGX+pNa1KkWMgtkvsa6zF1QQ==',
 'redirectAfterLoginReg': '/',
 'fusionauth.timezone': 'Europe/Berlin',
 'requiredCookie': 'true',
 'federated.csrf': 'fRY-3hq7xxxm0N8N',
 'fusionauth.sso': 'AtXPmHe_3P_J_xBg9TT915Qg-hR3fZfjlS4PFnYTzMW_ngr_4NvH6K0s',
 'fusionauth.remember-device': 'QkJCAS9SrgDyb9xwxuMeEix2KN1FluQWtfJVixva_zw-kOvvD4b5jQ==',
 'bm_sv': 'C8C2DF4C2F916216A1949ED9E4DF61ED~YAAQyqEkF1GwamCXAQAABCRsgxyrkQQ5bnQsIsrKRSOFCNWwzdqHP6ZchAvWRXm0EAzlFKYadjnKlFLv1L5SvPfu/FloncTky5kyTArZ5Ngxm8/lq5RSN0dHf3Sy8L5Xh1Dw5MaUodQtf9zG/BL+5CoxzrEqbSDWlFnOy6uFBxfnhtfQpNNU9nJ0k7O1EQKaJwBiesZ/FUIh7BfO7+T5fQqsyXANK2F2eHSNKgHwjCMS4xwJVmZhrpQrep4fQpY=~1'}

     

    # Payload expects userId and domain
    payload = {"email": email.strip() if email else ''}

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/json',   
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        # Add other headers if needed
    }

     

    try:
        response = requests.post(url, headers=headers,cookies=cookies, json=payload, timeout=30)
        response.raise_for_status()  # Raise error for bad HTTP status
    except Exception as e1:
        try:
            return {"error":  'invalid method!', "status_code": response.status_code, "message": "BONIFY.de loads dynamically. visit via selenium https://my.bonify.de/login to start.", 'available': None}
        except Exception:
            return {"error":  'invalid method!', "status_code": None, "message": "BONIFY.de loads dynamically. visit via selenium https://my.bonify.de/login to start.", 'available': None}
    try:
        # The response should be JSON
        result = response.json()
        return  {"error":  None, "status_code": response.status_code, "message": result , 'available': None}

    except Exception:
        try:
            soup=BeautifulSoup(response.content,'html.parser') 
            if  ' '.join(soup.find('h1').text.strip().split()).startswith('404'):
                return {"error":  'invalid method! '+ ' '.join(soup.find('h1').text.strip().split()), "status_code": 404, "message": "BONIFY.de loads dynamically. visit via selenium https://my.bonify.de/login to start.", 'available': None}
            else:
                return {"error":  'invalid method! '+' '.join(soup.find('h1').text.strip().split()) if soup.find('h1') else  ' '.join(soup.find('body').text.strip().split()), "status_code": 404, "message": "BONIFY.de loads dynamically. visit via selenium https://my.bonify.de/login to start.", 'available': None}
                
        except Exception as e2:
            return    {"error":  str(e2), "status_code": response.status_code, "message": "BONIFY.de loads dynamically. visit via selenium https://my.bonify.de/login to start.", 'available': None}
            

    class  bonifyChecker:
        def __init__(self, email: str = None ):
            self.email = email.strip() if email else None
            self.source = 'bonify.de'
            call = check_if_email_exists_in_bonify_de_via_requests(email=self.email)
            self.error = call['error']
            self.status_code = call['status_code']
            self.message = call['message']
            self.available = call['available']
        def __repr__(self):
            return f"{self.available}"

    test = bonifyChecker(emailemail)
    return test #{'email': 'a@gmail.com', 'source': 'okx.com', 'error': 'invalid method', 'status_code': 405, 'message': "OKX has no exposure of the 'email' other users, so None method will work without direct access into the database.", 'available': None}


#check_if_email_exists_in_bonify_de_via_requests_to_check_if_method_loads_dynamically_as_a_class(email='anon@example.com')