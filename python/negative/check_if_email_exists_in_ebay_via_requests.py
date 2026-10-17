def check_if_email_exists_in_ebay_via_requests(email: str = None, cookies: dict = {}, headers: dict = {}) -> dict:
    import requests
    url = "https://signin.ebay.com/signin/srv/identifer"

    # Default headers (can be overridden)
    default_headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://signin.ebay.com",
        "referer": "https://signin.ebay.com/ws/eBayISAPI.dll",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-full-version": '"137.0.7151.104"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"19.0.0"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "x-ebay-c-trackable-id": "01JY0DGV1S1YYQQ5ASNCWFC2FK",
        "x-ebay-requested-with": "XMLHttpRequest",
        "x-requested-with": "XMLHttpRequest",
    }

    # Merge input headers into default headers (input overrides default)
    merged_headers = {**default_headers, **headers}
    cookies = {
    "s": "CgAD4ACBoU3RrODBkODY2NzcxOTcwYTg5MzQ3ZTVmYTUzZmZmZTA5NTe1VIcr",
    "cid": "x1BnuR6lwazK4KJV#403179862",
    "__uzma": "9df7398b-e676-48d6-9dda-3c1d20ecc0e5",
    "__uzmb": "1750213355",
    "__uzmc": "502791071621",
    "__uzmd": "1750213355",
    "__uzme": "8389",
    "__uzmf": "7f60004518689e-d2d6-4ab3-babe-88644f43e8fe17502133550900-3eb10f579e6bd14810",
    "ak_bmsc": "7484573176DF107E2AB56A0EEAD58085~000000000000000000000000000000~YAAQ2aDVF5ruwnqXAQAAKGfYgBwGKT8Til/XMTJF274BzVhPN3wBY3/lzvt3kk3ywRwVvPgR7besLZlhm5+/Obq0mkQoms8/hyrG/PKVmQqtInMkhMpkuxBnY290Z8+/Nz8AbjUflbQOzKTcEiGB6RWR4rMdXv3iX0CmI5Br8mnx4BonF+9al1+jc2RRw9CS7EXy4ntEwDvOJRgKdpdglbaTmA59DKIgKWfQmaLMONfC0nZ8RB4/0b7KFonQCQx2wN6zhqgLkEgX8Hpsqm6b8jtmHKbAYEpKycFCv2b2HY3JsQXLRGjqD6wUewehY99Q1ovn92/PwvYnud9hSlv9vNHmMPVsADzych+AeTUC8VE8OlbPHXswC5jnyEiYcUsK4NorPkp9qCUu",
    "__ssds": "2",
    "__ssuzjsr2": "a9be0cd8e",
    "__uzmaj2": "36e28407-722a-4a89-8bcb-8e237bf5c558",
    "__uzmbj2": "1750213356",
    "__uzmcj2": "443621061594",
    "__uzmdj2": "1750213356",
    "__uzmlj2": "yV0WYD3mRq2h2tBN140OhpOCPVW3eE9tHSm6Osyrh84=",
    "__uzmfj2": "7f60004518689e-d2d6-4ab3-babe-88644f43e8fe17502133563270-2e87e03278b09cc610",
    "__deba": "PZ3pwyQ_HpANyaiFhmJBTiEiddwibwZBvlvE_F3uBv8cEihxvp-u06kI_kAPns5LXR8UW1J2_XMwSXzXGqPFGLENo_nd2hcnTufSCXwCbwpyzPExkL13JvypXigpBjffVpzkKhP71dhnjW8J9qyCkQ==",
    "nonsession": "BAQAAAZZay1gcAAaAADMABWozVnIxMDExNQDKACBsFInyODBkODY2NzcxOTcwYTg5MzQ3ZTVmYTUzZmZmZTA5NTcAywABaFIp+jTKdOxQKhc1/9hWawF+psISqBkSPg**",
    "dp1": "bu1p/QEBfX0BAX19AQA**6c1489f2^pbf/%23200000004000000000000000000046a335672^tzo/1a4685230fb^bl/DE6c1489f2^",
    "ds2": "sotr/bGivJzzzzzzz^",
    "ebay": "^js=1^sbf=#000000^psi=A2GZ8VTs*^"
}


    # Payload for the POST request (form data)
    payload = {
        "identifier": email.strip() if email else '',
        "srt": "01000a000000505c93f972b16c19ffb6d34ce640f74681b7c3d9be42685adf26ecc4504e5fdf6c1af0305b7f79b3534b4702497664a452951aeee48a1c64d10c48cbebe209e125773f265886c7fb756db988141da004c3",
        "webAuthNOptedInKeys": "",
        "webAuthNCredCheck": "false",
        "flowType": "PSI",
    }

    try:
        response = requests.post(url, cookies=cookies, headers=merged_headers, data=payload, timeout=10)

        #print(response.status_code)
        response.raise_for_status()
    except Exception as e1:
        try:
            return {"error": str(e1), "status_code": response.status_code, "message": None, "available": None}
        except Exception:
            return {"error": str(e1), "status_code": "", "message": None, "available": None}
            
    try:
        dictionary = response.json()
        #print(dictionary)
    except Exception as e2:
        #print(f"JSON decode error: ")
        try:
            return {"error": str(e2) , "status_code": response.status_code, "message": response.text, "available": None}
        except Exception:
            return {"error": str(e2), "status_code": "", "message": None, "available": None}
    try:
        # Check for 'webAuthnModel' key and nested 'userUniqueId'
        webAuthnModel = dictionary.get('webAuthnModel', {})
        if 'userUniqueId' in str(webAuthnModel):
             # Email exists / is registered
            return {"error": None, "status_code": response.status_code, "message": dictionary['webAuthnModel'], "available": 0}
        else:
            # Email does not exist / available
            return {"error": None, "status_code": response.status_code, "message": dictionary['webAuthnModel'], "available": 1}
    except Exception as e3:
        try:
            return {"error": str(e3), "status_code": response.status_code, "message": dictionary , "available": None}
        except Exception:
            try:
                return {"error": str(e3), "status_code": response.status_code, "message": None, "available": None}        
            except Exception:
                return {"error": str(e3), "status_code": None, "message": None, "available": None}        
                
             
class ebayChecker:
    def __init__(self, email: str = None ):
        self.email = email.strip() if email else None
        self.source = 'ebay.com'
        call = check_if_email_exists_in_ebay_via_requests(email=self.email)
        self.error = call['error']
        self.status_code = call['status_code']
        self.message = call['message']
        self.available = call['available']

    def __repr__(self):
        return f"{self.available}"

#example usage:
#test1 = check_if_email_exists_in_ebay_via_requests(email='ioanna.pipili@web.de')#({'error': '400 Client Error: Bad Request for url: https://signin.ebay.com/signin/srv/identifer',  'status_code': 400,  'message': None,  'available': None},
#test2 = check_if_email_exists_in_ebay_via_requests(email='a00040408@gmail.com')#({'error': '400 Client Error: Bad Request for url: https://signin.ebay.com/signin/srv/identifer',  'status_code': 400,  'message': None,  'available': None},