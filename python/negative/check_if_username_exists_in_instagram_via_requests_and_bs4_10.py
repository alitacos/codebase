def check_if_username_exists_in_instagram_via_requests_and_bs4(username:str='',retries:int=3, delay: int = 2,url : str = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/" ,headers:dict={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "*/*","Content-Type": "application/x-www-form-urlencoded","X-Requested-With": "XMLHttpRequest","X-CSRFToken": "gT5xjdTL4X7WoR6XbHZVdj","X-IG-App-ID": "936619743392459","Origin": "https://www.instagram.com","Referer": "https://www.instagram.com/accounts/emailsignup/"},cookies:dict={},allow_redirects:bool=False )->dict:
    import time
    import requests
    from bs4 import BeautifulSoup
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None,"available":False,"exists":False,"isDeleted":None}
    for _ in range(retries):
        #cookies = {"csrftoken": "gT5xjdTL4X7WoR6XbHZVdj","ig_did": "BEC6C4DA-2C41-47D0-BFEC-B2540B78F3F9","mid": "aTGvXAALAAEapmIPfUJQQr6TztCC","datr": "XK8xaRQ37p3s8Mo21ir-9l1c","wd": "715x681"}
        try:
            r = requests.post(url, data={"email":'',"failed_birthday_year_count": "{}","first_name": "","username": str(username).strip(),"opt_into_one_tap": "false","use_new_suggested_user_name": "true","jazoest": "21895"}, headers=headers, cookies=cookies,allow_redirects=allow_redirects)
            if r.status_code == 200:
                response = r.json()
                erros_info = response.get('errors',{})
                username_info = erros_info.get('username',[])
                for username_item in username_info:
                    if isinstance(username_item,dict):
                        msg = username_item.get('message','')
                        code = username_item.get('code','')    
                        if code == 'username_invalid' or msg == 'A user with that username already exists.':
                            return {'error': False, "status": r.status_code, "username": username, "content": response, "title": None,"available":False,"exists":True,"isDeleted":None}
                if erros_info and not username_info:
                    return {'error': False, "status": r.status_code, "username": username, "content": response, "title": None,"available":True,"exists":False,"isDeleted":None}
            last_error = f'unexpected status_code {r.status_code}'
            time.sleep(delay)
            continue
        except Exception as e:
            last_error = str(e)
            time.sleep(delay)
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None,"available":None,"exists":None,"isDeleted":None}
#example usage:
#check_if_username_exists_in_instagram_via_requests_and_bs4(username='alitakos90papatoliosalex')
