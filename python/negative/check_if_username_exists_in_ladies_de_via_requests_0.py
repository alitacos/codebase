def check_if_username_exists_in_ladies_de_via_requests(username:str='',retries:int=3, delay: int = 2,url:str="https://login.ladies.de/api/validate/registration?locale=de", headers:dict={"Accept": "application/json, text/plain, */*","Accept-Encoding": "gzip, deflate, br, zstd","Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7","Referer": "https://login.ladies.de/register","Sec-CH-UA": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',"Sec-CH-UA-Mobile": "?0","Sec-CH-UA-Platform": '"Windows"',"Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-origin","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","X-Requested-With": "XMLHttpRequest","X-XSRF-TOKEN": "eyJpdiI6InZEOHBFQ2N0MzVyNlQvMzhaeGIzWWc9PSIsInZhbHVlIjoiaVZqY092VklPYTBHK2dRVEN3OHVXZnBrQm5wM01ONDBwN3JXM3h5a0VQK0FwK25OWEVWcFlTTWRXWmZyRDdZVWt4UTB5emE4YlVpdHgxbEdjVUlndW8zRytycjJKblU2Z2gwU3dRRlpqMTRlVDVVM3MwNUJaS3k5WmUwK2RwNmIiLCJtYWMiOiJhYjkwZjI3OTY4YzJmZjQyZTMwNDJmMzJkMDc5MjY0OWU5OTg1MmQxMGFlZjM4MTA1YmJlMWE5MTBmM2RlZGQ2IiwidGFnIjoiIn0=",})->dict:
    import time
    import requests
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None,"available":False,"exists":False}
    for _ in range(retries):
        try:
            payload = {"_token": "ahfwDBub7MZtsvNQhzF8Ai5b9VyMjFizySCcWlCg","my_name_ZabeTCUgoDL6jrvQ": "","valid_from": "eyJpdiI6IlVDL0NvWWNZWXI3N0pJeXJWd1g0ZlE9PSIsInZhbHVlIjoiSGpjaS9lZUZ6YXRDTVJJNUtZbTNQQT09IiwibWFjIjoiOTc2M2Y5MDQxNWIzM2E3ZDI5MjcyZTMzMTJlOGEyMDUxMGZiMzRhZjFjZWJiMTYxY2IyZjliZWM3N2IxZTM4NSIsInRhZyI6IiJ9","name": str(username).strip(),"email": "","password": "","password_confirmation": "",}
            response = requests.post( url, headers=headers, data=payload)
            if response.status_code == 422:
                info =  response.json()
                errors = info.get('errors',{}) if info else {}
                name_errors = errors.get('name',[])
                message = info.get('message','')
                if 'Dieser Name ist bereits vergeben.' in name_errors or 'Dieser Name ist bereits vergeben.' in message:
                    return {"error":False ,"status": 422,"username": username, "content": '\n'.join([i for i in response.text.replace('\t','\n').strip().split('\n') if i and i.strip()]) if response.text else None , "title": None,"available":False,"exists":True}
                else:
                    return {"error":False ,"status": 422,"username": username, "content": '\n'.join([i for i in response.text.replace('\t','\n').strip().split('\n') if i and i.strip()]) if response.text else None , "title": None,"available":True,"exists":False}
            return {'error':f'unexpected status_code {response.status_code}',"status": response.status_code,"username": username,"content": response.text , "title": None,"available":None,"exists":None}
        except Exception as e:
            last_error = str(e)
            time.sleep(delay)
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None,"available":None,"exists":None}

# Example usage:
#check_if_username_exists_in_ladies_de_via_requests(username='anonymous')
