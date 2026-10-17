import requests

def check_if_email_exists_in_twitter_as_boolean(email: str = '') -> bool:
    if not email:
        return False
        
    url = f'https://x.com{email}'
    
    # Erweiterte Header, um modernen Schutzmechanismen zu entgehen
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        # Falls X mit einem HTTP-Fehlercode (z.B. 403, 429) antwortet
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
        # Fängt den Fehler ab, wenn HTML statt JSON zurückgegeben wird
        print(f"❌ Fehler: Keine gültige JSON-Antwort von X empfangen (Status: {response.status_code}).")
        print(f"Inhalt der Antwort (HTML/Text): {response.text[:500]}")
        data = {
            "error": "Keine JSON-Antwort (HTML-Sperre/Cloudflare)", 
            "status_code": response.status_code, 
            "valid": False, 
            "msg": None, 
            "taken": False
        }
    except Exception as e:
        # Allgemeiner Fallback für Verbindungsfehler
        data = {
            "error": str(e), 
            "status_code": 500, 
            "valid": False, 
            "msg": None, 
            "taken": False
        }
        
    print("Resultat-Daten:", data)
    return bool(data.get('taken', False))

# Test
#print(check_if_email_exists_in_twitter_as_boolean(email='f'))
