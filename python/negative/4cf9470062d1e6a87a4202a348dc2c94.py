def check_if_email_exists_on_instagram_via_requests(email: str='', retries:int=3,delay:int=2, csrf_token: str= 'QdU1jSZtmXQDGNEZSIko9RyaULj',url :str= 'https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/',   headers : dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36', 'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.9', },  **kwargs) -> dict:
    import requests
    import time
    if not email or not isinstance(email,str) or not email.strip():
        return {'email':email,'error': 'ValueError', 'status_code': None, 'message': 'Invalid <email>', 'available': False,'exists':False, 'isdeleted':False}
    try:
        headers['X-CSRFToken'] = csrf_token 
    except Exception as e1:
        return {'email':email,'error': e1, 'status_code': None, 'message': None, 'available': None,'exists':None, 'isdeleted':None}

    error_message = None
    status_code = None
    for attempt in range(int(retries)):
        try:
            query_payload = {'email_or_username': email.strip(), 'jazoest': '22739'}
            response = requests.post(url, headers=headers,   data=query_payload,**kwargs)
            status_code  = response.status_code
            if f'We sent an email to {email} with a link to get back into your account.' in str(response.json()):
                return {'email':email,'error': False, 'status_code': status_code, 'message': response.json()['toast_message'], 'available': False,'exists':True, 'isdeleted':None}
            elif 'No users found' in str(response.json()):
                return {'email':email,'error': False, 'status_code': status_code, 'message': response.json()['message'], 'available': True,'exists':False,'isdeleted':None}
            elif 'CSRF token missing or incorrect' in str(response.json()):
                return {'email':email,'error':True, 'status_code': response.status_code, 'message':  response.json()['message'], 'available': None ,'exists':None,'isdeleted':None}

        except Exception as e:
            error_message = e
        if attempt < retries - 1:
            time.sleep(delay)
            continue  # Simulate retry by continuing the loop (and reattempting the request)
    return   {'email':email,'error': error_message.__class__.__name__ if error_message else True, 'status_code': status_code, 'message': str(error_message) if error_message else None, 'available': None,'exists':None, 'isdeleted':None}

 