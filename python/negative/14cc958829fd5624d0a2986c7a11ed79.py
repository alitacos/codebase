def check_if_email_exists_on_instagram_via_requests(email: str='', retries:int=3,delay:int=2, csrf_token: str= 'QdU1jSZtmXQDGNEZSIko9RyaULj',url :str= 'https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/',   headers : dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36', 'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.9', },  **kwargs) -> dict:
    """
    Checks if the given email exists on Instagram by making a request to their account recovery API.

    **Note**: This approach rarely works unless you have a valid session or CSRF token. Instagram may block requests if the token is invalid or expired, or if there are too many requests in a short period.

    Args:
        email (str): The email address to check for existence (Defaults to '')
        retries (int): The number of retries in case of failure (Defaults to 3)
        delay (int): The delay between retries in seconds (Defaults to 2)
        csrf_token (str): The CSRF token required for the request (Defaults to 'QdU1jSZtmXQDGNEZSIko9RyaULj')
        url (str): The API URL for the Instagram account recovery (Defaults to 'https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/')
        headers (dict): The headers to send with the request, including User-Agent and Accept (Defaults to a set of typical headers)
        
    Returns:
        dict: A dictionary containing the result, including availability, error, status code, etc.

    Example usage:
        >>> result = check_if_email_exists_on_instagram_via_requests(email='example@example.com', retries=3, delay=2, csrf_token='valid_token', url='https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/', headers={'User-Agent': 'Mozilla/5.0 ...'})
    """
    import requests
    import time
    import json # Added missing import
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
            response = requests.post(url, headers=headers, data=query_payload, **kwargs)
            status_code = response.status_code

            # Handle possible successful responses
            if response.status_code == 200:
                try:
                    json_response = response.json()  # Attempt to parse the JSON response
                except json.JSONDecodeError as e:
                    return {'email': email, 'error': 'JSONDecodeError', 'status_code': status_code,'message': 'Response body is not valid JSON', 'available': None, 'exists': None, 'isdeleted': None}
                if f'We sent an email to {email} with a link to get back into your account.' in str(json_response):
                    return {'email': email, 'error': False, 'status_code': status_code, 'message': json_response.get('toast_message', ''),'available': False, 'exists': True, 'isdeleted': None}
                elif 'No users found' in str(json_response):
                    return {'email': email, 'error': False, 'status_code': status_code, 'message': json_response.get('message', ''),'available': True, 'exists': False, 'isdeleted': None}
                elif 'CSRF token missing or incorrect' in str(json_response):
                    return {'email': email, 'error': True, 'status_code': status_code, 'message': json_response.get('message', ''),'available': None, 'exists': None, 'isdeleted': None}
            else:
                error_message = f"Unexpected status code: {status_code}"
        except requests.exceptions.RequestException as e:
            error_message = str(e)

        # Retry on error, unless it's the last attempt
        if attempt < retries - 1:
            time.sleep(delay)

    # If all retries fail, return the error details
    return {'email': email, 'error': error_message or 'Request failed', 'status_code': status_code,'message': str(error_message), 'available': None, 'exists': None, 'isdeleted': None}