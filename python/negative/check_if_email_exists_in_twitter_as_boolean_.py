import requests

def check_if_email_exists_in_twitter_as_boolean(email: str = '') -> bool:
    if not email:
        return False
        
    url = f'https://api.x.com/i/users/email_available.json?email={email}'
    
    # Diese Header simulieren eine legitime Anfrage eines Standard-Webbrowsers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://x.com/',
        'Origin': 'https://x.com',
        'DNT': '1'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        dict_response = response.json()
        
        # Bereinigung des Antworttextes (Entfernt Punkte am Ende für exakten Abgleich)
        msg = dict_response.get('msg', '').rstrip('.')
        
        data = {
            "error": None, 
            "status_code": response.status_code, 
            "valid": dict_response.get('valid', False), 
            "msg": dict_response.get('msg'), 
            "taken": dict_response.get('taken', False)
        }
    except Exception as e:
        data = {
            "error": str(e), 
            "status_code": vars(e).get('response', {}).get('status_code', 500) if 'response' in vars(e) else 500, 
            "valid": False, 
            "msg": None, 
            "taken": False
        }
        
    print(data)
    return bool(data.get('taken', False))

# Beispiel-Aufrufe:
#print(check_if_email_exists_in_twitter_as_boolean(email='f'))
#print(check_if_email_exists_in_twitter_as_boolean(email='anon@grr.la'))
#print(check_if_email_exists_in_twitter_as_boolean(email='alitakos9s0@gmail.com'))
