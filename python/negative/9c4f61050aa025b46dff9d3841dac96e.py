def check_if_email_exists_on_instagram_via_requests_using_forgot_passwort_recovery_method(email:str='',csrf_token:str='',cookies:dict={},headers:dict={},payload:dict= {}) -> dict:
    import requests
    url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
    if not cookies:
        cookies = {
    #"csrftoken": "QdU1jSZtmXQDGNEZSIko9RyaULjbUZ26",
    #"ig_did": "AF72D69E-A8AE-4D77-B7C5-4BED3C04619A",
    #"mid": "aFBQOQALAAG-7p-hT6pUQb6WlDzk",
    #"datr": "OVBQaDl9XJU8lUc6cr2NYRIV",
    #"dpr": "1.25",
    #"wd": "638x730"
    }
    if not headers:
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        #"Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrf_token if csrf_token else 'QdU1jSZtmXQDGNEZSIko9RyaULj',#"QdU1jSZtmXQDGNEZSIko9RyaULjbUZ26",
        #"X-Instagram-AJAX": "1023871506",  # Must match your current session
        #"X-IG-App-ID": "936619743392459",
        #"X-Requested-With": "XMLHttpRequest",
        #"X-ASBD-ID": "359341",
        #"X-IG-WWW-Claim": "0",  # Often required even if set to "0"
        #"X-Web-Session-ID": "rxqlco:qckg4x:tdao81",
        #"Origin": "https://www.instagram.com",
        #"Referer": "https://www.instagram.com/accounts/password/reset/",
        #"Sec-Fetch-Site": "same-origin",
        #"Sec-Fetch-Mode": "cors",
        #"Sec-Fetch-Dest": "empty"
    }
    if not payload:
        payload = {"email_or_username": email.strip(), "jazoest": "22739"}
        
    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=payload)

        if f'We sent an email to {email} with a link to get back into your account.' in str(response.json()):
            return {"error": None, "status_code": response.status_code, "message": response.json()['toast_message'], 'available': 0}
        elif 'No users found' in str(response.json()):
            return {"error": None, "status_code": response.status_code, "message": response.json()['message'], 'available': 1}
        elif 'CSRF token missing or incorrect' in str(response.json()):
            return {"error": response.json()['message'], "status_code": response.status_code, "message": None, 'available': None}    
        else:
            return {"error":'unknown error', "status_code": response.status_code, "message": response.json(), 'available': None}    
            
    except Exception as e:
        return {"error": str(e), "status_code": None, "message": None, 'available': None}

#example usage:
#check_if_email_exists_on_instagram_via_requests_using_forgot_passwort_recovery_method(email='example@example.com')