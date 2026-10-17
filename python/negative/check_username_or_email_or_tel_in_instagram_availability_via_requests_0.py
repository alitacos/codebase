def check_username_or_email_or_tel_in_instagram_availability_via_requests(username:str='',phoneORemail:str='')->dict:
    #cookies = {"csrftoken": "gT5xjdTL4X7WoR6XbHZVdj","ig_did": "BEC6C4DA-2C41-47D0-BFEC-B2540B78F3F9","mid": "aTGvXAALAAEapmIPfUJQQr6TztCC","datr": "XK8xaRQ37p3s8Mo21ir-9l1c","wd": "715x681"}
    import requests
    url = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/"
    if phoneORemail:
        if '@' not in str(phoneORemail):
            if not str(phoneORemail).strip().replace('+','').isdigits():
                return {'error':'please enter a valid email address or phone number','response':None}
            if str(phoneORemail).strip().isdigits():
                phoneORemail = phoneORemail.strip().replace(' ','') 
    if username:
        if '@' in str(username) or not isinstance(username, (str,None)):
            return {'error':'please enter a valid username','response':None}
    if  not username and not phoneORemail:
        return {'error':'please enter a valid input <username> or <phoneORemail>','response':None}
    try:
        r = requests.post(url, data={"email": phoneORemail.strip(),"failed_birthday_year_count": "{}","first_name": "","username": str(username).strip(),"opt_into_one_tap": "false","use_new_suggested_user_name": "true","jazoest": "21895"}, headers=headers, cookies=cookies)
        return{'error':False, 'response': r.text  }
    except Exception as e:
        return {'error':e, 'response':None}
