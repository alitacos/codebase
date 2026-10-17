def check_if_email_exists_aready_in_here_com_as_boolean(email:str='') -> bool:
    if not email:
        return False

    def check_if_email_exists_in_here_com_via_requests(email: str = None,cookies=None,headers=None,typ=None )->dict:
        """        Check if an email user ID exists in here.com registration system.        """
        import json
        import requests
        from bs4 import BeautifulSoup
        if not email:
            raise ValueError("Email must be provided")
        url = "https://account.here.com/api/account/sign-in-user-info"
        # Payload expects userId and domain
        payload = {"email": email.strip() if email else ''}   
        if not headers:
            headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'x-client':'YQijV3hAPdxySAVtE6ZT',
        'x-correlation-id':'HAWeb-8f236078-d99b-472e-b2e2-16bb64b76d8e',
        'x-csrf-token':'6c805f58112fcb9469d2d060d6def9be1624a644482c78193ddfd4acd89c9fb4718283265cb24db23824ce124bb68d539df983e75bbef783a4fa401bf7ff6620'}
    # If you need cookies, define them like this:
        if not cookies:
            cookies = {"__Host-here._csrf":"s%3A6c805f58112fcb9469d2d060d6def9be1624a644482c78193ddfd4acd89c9fb4718283265cb24db23824ce124bb68d539df983e75bbef783a4fa401bf7ff6620%7C1d2717c9eda6f2dc66ebc60a474313f6413baa57a99a2073c841801b63c0afb1.2omyiW2QS0ksUuTBCxC8Unl1NLvzd6DvPIs13WPylE0; here_csrf_token=6c805f58112fcb9469d2d060d6def9be1624a644482c78193ddfd4acd89c9fb4718283265cb24db23824ce124bb68d539df983e75bbef783a4fa401bf7ff6620"    }
     
        try:
            response = requests.post(url, headers=headers, cookies=cookies, json=payload, timeout=30)
            response.raise_for_status()  # Raise error for bad HTTP status
        except Exception as e1:
            try:
                return {"error": 'invalid method', "status_code": response.status_code, "message": "here.com has no exposure of the 'email' availability via requests", 'available': None, "exists":  None}
            except Exception:
                return {"error": 'invalid method', "status_code": None, "message": "here.com has no exposure of the 'email' availability via requests", 'available': None ,"exists": None}
        try:
            # The response should be JSON
            result = response.json()  # This gives a dictionary directly, no need for json.loads()         
            return {"error": None, "status_code": response.status_code, "message": result, 'available': 0 if result['accounts'][str(typ)]['exist'] else 1,"exists":True if  result['accounts'][str(typ)]['exist'] else False}
        except Exception as e1:
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                # If soup.text is a string that looks like JSON, we need to parse it into a dict
                if soup.text.strip().startswith('{') and soup.text.strip().endswith('}'):
                    result = json.loads(soup.text)  # Parse the string as JSON
                    return {"error": str(e1), "status_code": response.status_code, "message": result, 'available': None,'exists': None}
                else:
                    return {"error": str(e1), "status_code": response.status_code, "message": soup.text, 'available': None, 'exists': None,}
            except Exception as e2:
                return {"error": str(e2), "status_code": response.status_code, "message": None, 'available': None ,'exists': None}

    class single_here_com_Checker:
        def __init__(self, email: str = None, typ='platform'):
            # Ensure typ is a string, not a list
            if isinstance(typ, list):
                typ = typ[0]  # Use the first element if it's a list
            self.email = email.strip() if email else None
            self.source = 'here.com'
            call = check_if_email_exists_in_here_com_via_requests(email=self.email, typ=typ)
            self.error = call['error']
            self.status_code = call['status_code']
            # Here, we're assigning the account info directly, not using a dict key of a dict
            self.message =  call['message']['accounts'][str(typ)]  
            self.available = call['available']
        def __repr__(self):
            return f"{self.available}"
    class hereChecker:
        def __init__(self, email: str = None,types=None):
            if not types:
                types= ['platform', 'developer']
            self.items = [single_here_com_Checker(email=email, typ=i) for i in types]
            self.platform = self.items[0].__dict__ if 'platform'  in types else None
            self.developer = self.items[-1].__dict__ if 'developer'  in types else None 
        def __repr__(self):
            return self.items
    # Example usage
    test =   hereChecker(email=email)
    platform =  test.platform.get('message',{}).get('exists')
    developer =  test.developer.get('message',{}).get('exists')
    if platform or developer:
        return True    
    return False
 
#example usage:
#check_if_email_exists_aready_in_here_com_as_boolean('example@here.com')
# unknown if works.. must dubble check later