def check_if_email_exists_in_appleid_via_requests_and_bs4(email:str=None, cookies:dict={},headers:dict={},payload:dict={} ):
    import requests
    from bs4 import BeautifulSoup
 
    url='https://appleid.apple.com/account/validation/appleid'
    headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "connection": "keep-alive",
    "content-length": "38",  # optional, requests manages it automatically
    "content-type": "application/json;charset=UTF-8",
    "host": "appleid.apple.com",
    "origin": "https://appleid.apple.com",
    "referer": "https://appleid.apple.com/",
    "scnt": "kJEOTM5OUVFMUI4NTgyOEM5Njc0MDIwQ0Y4MkEzMEE2QjFBOUMxMzQ4N0FDMzk2REVEMjBGRjNCRTc2N0Y5QzgxOTI4NzkxNEE2RDMyQjE1M0UyRjY1QTIxMTY3RDgzNENBQzg3NDdBMjNDNkZFQTJCRjQ5QjYwRTYxM0I4MDA0RUE1QjBCNTlCNjkwQUMwMDE1MkZBRjA4NjFCMEIxNDU4RUExOUEzMUVFQkZFQjA0RDg1RjdGQzMwMzNGOUMxNzUwMkU3RDU4MzhFNEUwRkJDQjU1RkUxRTQ5RUU2MTgxQTlGQjg2N0ZBODBFRTExQ3w0AAABmZwzoY-_kdmoRwgBXxfJ_oaaqEI6_6z9BAuJxgwxmq3I1B-dKRz5iXNAf1htAAIqVv_6WzadHdTZAhXALKGN_R3WGcC2y4GOuudOKjDJMuo629x5XA",
    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "x-apple-i-fd-client-info": '{"U":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36","L":"de-DE","Z":"GMT+02:00","V":"1.1","F":"Nla44j1e3NlY5BNlY5BSs5uQ32SCVgdcK4J54Jc.MATMB5P_dhre9zH_y37lYKU.0Y.KI0TiNBpFeCiy3Ay32w9WY5BNlYJNNlY5QB4bVNjMk.3hb"}',
    "x-apple-i-timezone": "Europe/Berlin",
    "x-apple-id-session-id": "BD9399EE1B85828C9674020CF82A30A6B1A9C13487AC396DED20FF3BE767F9C819287914A6D32B153E2F65A21167D834CAC8747A23C6FEA2BF49B60E613B8004EA5B0B59B690AC00152FAF0861B0B1458EA19A31EEBFEB04D85F7FC3033F9C17502E7D5838E4E0FBCB55FE1E49EE6181A9FB867FA80EE11C",
    "x-apple-request-context": "create",
    "x-apple-widget-key": "af1139274f266b22b68c2a3e7ad932cb3c0bbe854e13a79af78dcc73136882c3",
}

    cookies = {
    "dslang": "DE-DE",
    "site": "DEU",
    "geo": "DE",
    "idclient": "web",
    "aidsp": "BD9399EE1B85828C9674020CF82A30A6B1A9C13487AC396DED20FF3BE767F9C819287914A6D32B153E2F65A21167D834CAC8747A23C6FEA2BF49B60E613B8004EA5B0B59B690AC00152FAF0861B0B1458EA19A31EEBFEB04D85F7FC3033F9C17502E7D5838E4E0FBCB55FE1E49EE6181A9FB867FA80EE11C",
    "adsv": "e5iEo8lX5g",
    "aid": "6E5C99E1864EFF7BC77FF2B4E680B2E0"
}

    payload = {
    
    "emailAddress": email if email else "" 
}

    
    try:
        response = requests.post(url, cookies=cookies, headers=headers, data=payload, timeout=10)

        #print(response.url)
        dictionary =  response.json() #{
        print(dictionary)
        
        if dictionary['used'] in [True,'true']:
            return  {"error":'invalid email' if dictionary['valid'] in [False, 'false'] else None, "status_code": response.status_code, "message": dictionary , 'available': 0}
        elif dictionary['used'] in [False,'false']:
            return  {"error":'invalid email' if dictionary['valid'] in [False, 'false'] else None, "status_code": response.status_code, "message": dictionary , 'available': 1}

        else:
            return  {"error":'unknown error! check captcha or cookies*', "status_code": response.status_code, "message": dictionary , 'available': None}
    except Exception as e2:
        try:
            return  {"error":str(e2), "status_code": response.status_code, "message": BeautifulSoup(response.text,'html.parser').find('h1').text if BeautifulSoup(response.text,'html.parser').find('h1') else BeautifulSoup(response.text,'html.parser').text, 'available': None}
        except Exception as e1:
            return  {"error":str(e1), "status_code": None, "message": None , 'available': None}
            
class appleidChecker:
    def __init__(self, email: str = None ):
        self.email = email.strip() if email else None
        self.source = 'apple.com'
        call = check_if_email_exists_in_appleid_via_requests_and_bs4(email=self.email)
        print(call)
        self.error = call['error']
        self.status_code = call['status_code']
        self.message = call['message']
        self.available = call['available']

    def __repr__(self):
        return f"{self.available}"


#test1 = check_if_email_exists_in_appleid_via_requests_and_bs4(email='ioanna.pipili@web.de')#{'error': 'Expecting value: line 1 column 1 (char 0)', 'status_code': 500, 'message': '', 'available': None}
#test2 = check_if_email_exists_in_appleid_via_requests_and_bs4(email='a00040408@gmail.com')#{'error': 'Expecting value: line 1 column 1 (char 0)', 'status_code': 500, 'message': '', 'available': None}
