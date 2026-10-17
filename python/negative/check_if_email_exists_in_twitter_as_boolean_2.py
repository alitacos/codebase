import requests

def check_if_email_exists_in_twitter_as_boolean(email: str = '') -> bool:
    if not email:
        return False
        
    # KORREKTUR: Die vollständige API-Route muss hier stehen
    url = f'https://x.com{email}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://x.com',
        'Origin': 'https://x.com',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
    
    # LÖSUNG FÜR CLOUDFLARE ONE:
    # Wenn Sie einen lokalen Proxy (z.B. Privoxy) oder z.B. Fiddler nutzen,
    # um Cloudflare zu umgehen, tragen Sie ihn hier ein. 
    # Um Cloudflare komplett zu umgehen, darf requests die System-Umgebungsvariablen nicht nutzen.
    
    session = requests.Session()
    session.trust_env = False  # Ignoriert die globalen Cloudflare-Proxies Ihres Systems!

    try:
        # Wir nutzen die bereinigte Session statt direkt requests.get
        response = session.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ X blockiert die Anfrage. Status Code: {response.status_code}")
            print(f"Antwort-Vorschau: {response.text[:200]}")
            return False
            
        dict_response = response.json()
        data = {
            "error": None, 
            "status_code": response.status_code, 
            "valid": dict_response.get('valid', False), 
            "msg": dict_response.get('msg'), 
            "taken": dict_response.get('taken', False)
        }
    except requests.exceptions.JSONDecodeError:
        print(f"❌ Fehler: Keine gültige JSON-Antwort (Status: {response.status_code}).")
        print(f"Inhalt der Antwort: {response.text[:500]}")
        data = {"error": "Keine JSON-Antwort", "status_code": response.status_code, "valid": False, "msg": None, "taken": False}
    except Exception as e:
        data = {"error": str(e), "status_code": 500, "valid": False, "msg": None, "taken": False}
        
    print("Resultat-Daten:", data)
    return bool(data.get('taken', False))

# Test
#print(check_if_email_exists_in_twitter_as_boolean(email='f'))
