def check_if_email_exists_in_appleid_via_requests_and_bs4(email:str=None, cookies:dict={},headers:dict={},payload:dict={} ):
    import requests
    from bs4 import BeautifulSoup
 
    url='https://appleid.apple.com/account/validation/appleid'
    if not headers:
        headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "connection": "keep-alive",
    "content-length": "38",  # optional, requests manages it automatically
    "content-type": "application/json",
    "host": "appleid.apple.com",
    "origin": "https://appleid.apple.com",
    "referer": "https://appleid.apple.com/",
    "scnt": "jRCN0E0RjQ0QjQ0QkU3OERGRDc1MEM0RjRFRjkyNjhFMzU3NzI0REU0QjQ2RjY4NTI3MENCQjU2REE3M0RGOENFMkUxQzcwOEEwMENCQzA4MkU5MzI1MDJGMURGRjdEQzFDMzQzNUFBQjNEM0RGOUQ2RTRGRTg3RjM3QzM2NEExRkYwOUFCOUY4RTk2NjgyMEMzNUZBNjQ5ODZBMjgxOTU1RDFBRjI0RkVFOTU1REFGMjY4Q0U2RDFFMzhDOTBGNUREOEQ0QTQ0QzJCOUYyRUIxNTYwMjUxQzFCOEFFMTQzRUU1MDcwOTlEODdFMTI5NHw0AAABl4P_btz-pJA-6wgqXOgEcYCGEVA5PogQ9U5wwO3XDHdooKQYNELZsqQZyMqUAAZyycoPsVeHY3-FQuJXmCpsH50t1KupNvzP7bNnPl_lLESvnH900Q",
    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "x-apple-i-fd-client-info": '{"U":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36","L":"de-DE","Z":"GMT+02:00","V":"1.1","F":"Nla44j1e3NlY5BNlY5BSs5uQ32SCVgdcK4J54Jc.MATMB5P_dhre9zH_y37lYKU.0Y.KI0TiNBpFeCiy3Ay32w9WY5BNlYJNNlY5QB4bVNjMk.3hb"}',
    "x-apple-i-timezone": "Europe/Berlin",
    "x-apple-id-session-id": "4B7A4F44B44BE78DFD750C4F4EF9268E357724DE4B46F685270CBB56DA73DF8CE2E1C708A00CBC082E932502F1DFF7DC1C3435AAB3D3DF9D6E4FE87F37C364A1FF09AB9F8E966820C35FA64986A281955D1AF24FEE955DAF268CE6D1E38C90F5DD8D4A44C2B9F2EB1560251C1B8AE143EE507099D87E1294",
    "x-apple-request-context": "create",
    "x-apple-widget-key": "af1139274f266b22b68c2a3e7ad932cb3c0bbe854e13a79af78dcc73136882c3",
}

    if not cookies:
        cookies = {
    "dslang": "DE-DE",
    "site": "DEU",
    "geo": "DE",
    "idclient": "web",
    "aidsp": "4B7A4F44B44BE78DFD750C4F4EF9268E357724DE4B46F685270CBB56DA73DF8CE2E1C708A00CBC082E932502F1DFF7DC1C3435AAB3D3DF9D6E4FE87F37C364A1FF09AB9F8E966820C35FA64986A281955D1AF24FEE955DAF268CE6D1E38C90F5DD8D4A44C2B9F2EB1560251C1B8AE143EE507099D87E1294",
    "adsv": "rJ7jv1IVE7",
    "aid": "B79597E0F41D008D88D365FCF35F3B61"
}

    payload = {
    
    "emailAddress": email if email else "" 
}

    
    try:
        response = requests.post(url, cookies=cookies, headers=headers, json=payload, timeout=10)

        #print(response.url)
        dictionary =  response.json() #{
        
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
        self.error = call['error']
        self.status_code = call['status_code']
        self.message = call['message']
        self.available = call['available']

    def __repr__(self):
        return f"{self.available}"

#example usage:
#test1 = appleidChecker(email='ioanna.pipili@web.de')
#test2 = appleidChecker(email='a00040408@gmail.com')
#test1.__dict__
