def check_if_email_exists_in_okx_via_requests(email: str = None,cookies=None,headers=None ):
    """
    Check if an email user ID exists in okx registration system.
    OKX has no exposure of the 'email' other users, so None method will work without direct access into the database.
    """
    import requests
    from bs4 import BeautifulSoup
    if not email:
        raise ValueError("Email must be provided")
    try:
        url="https://www.okx.com/de/account/login-pwd/forget?account="+email.split('@')[0] if email and len(email.split('@')) == 2 else ''+'%40' if email and len(email.split('@')) == 2 else '' + email.split('@')[-1]  if email and len(email.split('@')) == 2 else '' 
    except Exception:
        url="https://www.okx.com/de/account/login-pwd/forget?account="
        

     

    # Payload expects userId and domain
    payload = {"email": email.strip() if email else ''}

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/json',   
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        # Add other headers if needed
    }

     

    try:
        response = requests.post(url, headers=headers,cookies=cookies, json=payload, timeout=30)
        response.raise_for_status()  # Raise error for bad HTTP status
    except Exception as e1:
        try:
            return {"error":  'invalid method', "status_code": response.status_code, "message": "OKX has no exposure of the 'email' other users, so None method will work without direct access into the server´s internal database.", 'available': None}
        except Exception:
            return {"error":  'invalid method', "status_code": None, "message": "OKX has no exposure of the 'email' other users, so None method will work without direct access into the server´s internal database.", 'available': None}
    try:
        # The response should be JSON
        result = response.json()
        return  {"error":  None, "status_code": response.status_code, "message": result , 'available':  None}

    except Exception:
        try:
            soup=BeautifulSoup(response.content,'html.parser') 
            return    {"error":  None, "status_code": response.status_code, "message": soup.find('h1').text if soup.find('h1') else   None, 'available':  None}
        except Exception as e2:
            return    {"error":  str(e2), "status_code": response.status_code, "message": None, 'available': None}
            
     
            
# Example usage:
#result = check_if_email_exists_in_okx(email='anony@gmail.com',cookies=cookies)
#print(result)

class  okxChecker:
    def __init__(self, email: str = None ):
        self.email = email.strip() if email else None
        self.source = 'okx.com'
        call = check_if_email_exists_in_okx_via_requests(email=self.email)
        self.error = call['error']
        self.status_code = call['status_code']
        self.message = call['message']
        self.available = call['available']

    def __repr__(self):
        return f"{self.available}"
#example usage:
#test = okxChecker(email='a@gmail.com')#{'email': 'a@gmail.com', 'source': 'okx.com', 'error': 'invalid method', 'status_code': 405, 'message': "OKX has no exposure of the 'email' other users, so None method will work without direct access into the server´s internal database.",'available': None}
#check_if_email_exists_in_okx_via_requests(email='a@gmail.com')#{'error': 'invalid method', 'status_code': 405, 'message': "OKX has no exposure of the 'email' other users, so None method will work without direct access into the server´s internal database.",'available': None}
