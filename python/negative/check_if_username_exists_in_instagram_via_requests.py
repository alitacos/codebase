def check_if_username_exists_in_instagram_via_requests(username:str=''  )->dict:
    import requests
    url = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/"
    if not username or not isinstance(username, str) or not str(username).strip() or (username and  '@' in str(username)):
        return {'error':'please enter a valid username','response':None}     
    #cookies = {"csrftoken": "gT5xjdTL4X7WoR6XbHZVdj","ig_did": "BEC6C4DA-2C41-47D0-BFEC-B2540B78F3F9","mid": "aTGvXAALAAEapmIPfUJQQr6TztCC","datr": "XK8xaRQ37p3s8Mo21ir-9l1c","wd": "715x681"}
    try:
        r = requests.post(url, data={"email":'',"failed_birthday_year_count": "{}","first_name": "","username": str(username).strip(),"opt_into_one_tap": "false","use_new_suggested_user_name": "true","jazoest": "21895"}, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "*/*","Content-Type": "application/x-www-form-urlencoded","X-Requested-With": "XMLHttpRequest","X-CSRFToken": "gT5xjdTL4X7WoR6XbHZVdj","X-IG-App-ID": "936619743392459","Origin": "https://www.instagram.com","Referer": "https://www.instagram.com/accounts/emailsignup/"}, cookies={})
        return{'error':False, 'response': r.text  }
    except Exception as e:
        return {'error':e, 'response':None}

 