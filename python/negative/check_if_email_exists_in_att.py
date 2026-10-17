def check_if_email_exists_in_att_via_requests(username: str = '', cookies:dict=None, headers:dict=None, domain:str='')->dict:
    """
    Check if an email user ID exists in AT&T registration system.
    AT&T exposes limited email availability via an API endpoint.
    """
    import requests
    from bs4 import BeautifulSoup
    if not username:
        return {}
    url = "https://www.att.com/msapi/idmorch/registration/unauth/service/v2/checkAvailability"
    cookies ={
    "ixp": "5f990399-7cfd-4497-860a-0abc85f72638",
    "idse_stack": "aldc2",
    "UUID": "6852c3a2-1270-a95-53a0-53a0acfad593",
    "AKA_A2": "A",
    "akaalb_prod_onprem": "~op=prod_onprem_alb:prod-idp-aldc2|~rv=42~m=prod-idp-aldc2:0|~os=c2e53dcabb81922a188c759e7de57e2b~id=110a9f97195f8e6d799bc109b37a4ed8",
    "rxVisitor": "1750254498659N6L4Q07OQ4J38O5OQRR6KGNJCKKN41AK",
    "gtmuf": "azw2",
    "att-appshell-path": "/marketing/",
    "akaalb_prod_upperfunnel": "~op=prod_upperfunnel_alb:prod-upperfunnel-azw2|~rv=56~m=prod-upperfunnel-azw2:0|~os=c2e53dcabb81922a188c759e7de57e2b~id=dc679247830da9aec51ba4d6399963fa",
    "AMCVS_55633F7A534535110A490D44%40AdobeOrg": "1",
    "at_check": "true",
    "s_ecid": "MCMID%7C21470384101947023752698272765659515643",
    "mboxEdgeCluster": "37",
    "azure_ssaf_stack": "ssafwestus2",
    "at_geo": '{"latitude":50.12,"longitude":8.68,"countryCode":"DE","stateCode":"HE","city":"FRANKFURT"}',
    "CIP": "178.24.253.247",
    "_gcl_au": "1.1.947781622.1750254513",
    "gtmps": "aldc",
    "halologinstate": '{"final_url":["https://www.att.com/acctmgmt/signin?intent=ACCOUNTOVERVIEW"],"cid":"m14186"}',
    "gtmacct": "aze2",
    "AB_AKA-8357": "new_20241016",
    "gtmsales": "azw2",
    "akaalb_prod_sales": "~op=prod_sales_alb:prod-sales-azw2|~rv=8~m=prod-sales-azw2:0|~os=c2e53dcabb81922a188c759e7de57e2b~id=6e5098124c2db0af362eb407b8fa32ba",
    "ChatAB": "MEG",
    "QuantumMetricSessionID": "12b8f6c68338c95eaec440cc764abbef",
    "QuantumMetricUserID": "0403154ebd0da329a8720e03ce3d3d4b",
    "uws_storage": '"cookie"',
    "uws_prop_ui9uufma": '"n|session_timeout"',
    "uws_rate_comparators": '{"global":61509663}|session_timeout',
    "uws_ab_test": '12|session_timeout',
    "idp-source": "EMPTY",
    "aacState": "true",
    "cAuthNState": "en",
    "invoca_session": '{"ttl":"2025-07-02T13:48:37.119Z","session":{"invoca_id":"i-d9da73d4-b7f0-4eb6-fbfb-4b4ff476603f"},"config":{"ce":true,"fv":false,"rn":false,"ba":true}}',
    "Kd4zPCrb": "A6R-TIOXAQAAzH8C5RNTNp5lmLLZcNGEDQ8KpnOAFLygtJKXB7B95dR4-wsHAbIY_feucp7CwH8AAEB3AAAAAA|1|0|0b1e40fd120134372f9dc6c42ac5e95a5e37194b",
    "attathv": "012721",
    "PIM-SESSION-ID": "GPvaA09QLB9FugH1",
    "attpc-opt": '{"c":[{"type":"m","value":"y"},{"type":"n","value":"y"}],"consent":"a","gpc":"n"}',
    "__eoi": "ID=b9bd254302405511:T=1750254617:RT=1750254617:S=AA-AfjZfXvmHog4eKAkMc4Ru86Cb",
    "mbox": "session#fdf5eee50cd7413e92db737d2606379b#1750256482|PC#fdf5eee50cd7413e92db737d2606379b.37_0#1813499421",
    "_abck": "AA6D76F0078F854F6FDF69E9510F9C99~0~YAAQd48UAvpbd3iXAQAAfdNiR2xeHquY3eqJgfqAIlZOrTZt60_oDfaOSREpLx5dGpWwDiywmn5A7F1quVoTK38D5AKzvERbJwRQvhgxhjACd63Qdgh87dujsnHfqhtp63icofww6mJlIl4ek2vN00Sbb7rNJ9Syq21Xeipq9chJS2HLwvRDybdtxKN97FJrzo95yHp7abcuRp60Hkq-30xB9ptfd9S1FD35R7vtnMlPz6hT4tsH-csZT4gP0cGpHF0u1ip3Syz9jklNAXxbpV6lk8p0EKPqhzSOtm9giYOyYtxUqhd_i-5WmgkYd6XFXxMybFTVhNx3X9pGLs5nHyLYmd7rkCuBbtZT1jcgzywSjfGVY9VsacBQ==~0~A",
    "mboxData": "M6DCppGvnck7zyAVqfGz5iLxuMUVUNzz4A1VXBHq2xZZupzTYhxrOdUtQctGFdGRhgwDmh48fsoAKAIp8msykBlWzqZsoCTHDrhJKTjrMlqAfPcn1ouDNZj8Qz64YbDjrDD6TXXv4qV78pfsdQktFnw0rgV8wVsEKfi9oAHOvfHlqceBk2JRU_aVGOJqIrmmbR0DZKhwxudhtg_dY0vDNQZm43eR7cB6QTklXw+uVADpu9SiQN4niOb1xjATF1lJktDi8_HwS2RP8H6nRYM9H7vLfY9g9d2ECrnyXneEsYwmY2Iu9HCRSChR_fdoDKN9mvRhE4mRYWqBYbL8bAOIHuCkAhnYo4M_h54swg_Hg8QUyT6GeTmU+mj65_qtQg0F6Mxs78vfnFpmfbhlFzp1RmC6VjLTeWc8f0nFq0R2MhkTTlFxoKlybLN8I2_g==",
}
 
    payload  =  {
        "userId": username.strip() if username else '',
        "domain": domain
    }   

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'Referer':'https://www.att.com/acctmgmt/registration/opr/chooseID'}
    data = []
    try:
        response = requests.post(url, headers=headers, cookies=cookies, json=payload, timeout=3)
        response.raise_for_status()
    except Exception as e1:
        try:
            return {
                    "error": 'invalid method',
                    "status_code": response.status_code,
                    "message": "AT&T exposes email availability dynamically.",
                    'available': None
                }
        except Exception:
            return {
                    "error": 'invalid method',
                    "status_code": None,
                    "message": "AT&T exposes email availability dynamically.",
                    'available': None
                }
    try:
        return {
                "error": None,
                "status_code": response.status_code,
                "message": response.json(),
                'available':  None
            }
    except Exception:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            return {
                    "error": None,
                    "status_code": response.status_code,
                    "message": soup.text,
                    'available':   None
                }
        except Exception as e2:
            return {
                    "error": str(e2),
                    "status_code": response.status_code,
                    "message": None,
                    'available': None
                }
#example usage:
#check_if_email_exists_in_att_via_requests(email='anon',domain='att.com')
#check_if_email_exists_in_att_via_requests(email='anon',domain='currently.com')
#check_if_email_exists_in_att_via_requests(email='anon',domain='att.net')
     


     
class singleATTChecker:
    def __init__(self, email: str = None,domain:str='att.com'):
        self.email = email.strip() if email else None
        self.source = 'att.com'
        call = check_if_email_exists_in_att_via_requests(email=self.email,domain=domain)
        
        self.error = call['error']
        self.status_code = call['status_code']
        self.message = call['message']
        self.available = call['available']

    def __repr__(self):
        return f"{self.available}"
    
class AttChecker:
    def __init__(self, email: str = None,domains=None):
        if not domains:
            domains = ['att.net', 'currently.com']
        self.items = [singleATTChecker(email=email, domain=domain) for domain in domains][0] if len(domains)== 1 else [singleATTChecker(email=email, domain=domain) for domain in domains]
        try:
            self.att_net = self.items if 'att.net' in domains else None
        except Exception:
            self.att_net =   self.items if 'att.net' in domains else None
        try:
            self.currently = self.items[-1] if 'currently.com' in domains else None
        except Exception:
            self.currently =   self.items if 'currently.com' in domains else None

         
            
    def __repr__(self):
        if hasattr(self.items, '__iter__') and not isinstance(self.items, str):  # check if iterable, but not a string
            if len(self.items) == 1:
                return self.items.available
            else:
                return [i.available for i in self.items]
        else:
            return None  # return a single item

 
#test = AttChecker(email='a@gmail.com',domains=['att.net'])
#print(test.__dict__)