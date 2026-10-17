def check_if_username_exists_on_facebook_via_requests_1(username:str='')->dict:
    #first we visit url /login/identify/?ctx=recover&ars=facebook_login&from_login_screen=0 where we can input our email or phone query 
    url = 'https://www.facebook.com/login/identify/?ctx=recover&ars=facebook_login&from_login_screen=0'
    #next we post following with our query
    import requests
    try:
        response = requests.post('https://www.facebook.com/ajax/login/help/identify.php?ctx=recover', params={"ctx": "recover"}, data={"jazoest": "2984","lsd": "AdF_hfvq86k","email": query,"did_submit": "1","__user": "0","__a": "1","__req": "9","__hs": "20426.BP:DEFAULT.2.0...0","dpr": "1","__ccg": "EXCELLENT","__rev": "1030620896","__s": "5klll8:82busu:7fhs6a","__hsi": "7580003970653194271","__dyn": "7xeUmwkHg7ebwKBAg5S1Dxu13wqovzEdEc8uxa0CEbo1nEhw2nVE4W0qa0FE2awt81s8hwGwQw4iwBgao6C0Mo2swaO4U2zxe3C0D85a1qw8Xxm16wa-0raazo7u0zE2ZwrU6C0hq1Iw5lwnqwIwtU5K0UE62","__hsdp": "gQMT1GyQ6kkasWdGld2Vub89VHINE9XgaA0lW1xwqlrw2mU","__hblp": "0Xw9y1Aw2BU0z20GU0w60oK0cUw5Fw1Hi097w1na01m0wro0hIwv8yByoJ6w30Uy05pEeU","__spin_r": "1030620896","__spin_b": "trunk","__spin_t": "1764857203"})
        if "ServerRedirect" in response.text or "redirectPageTo" in response.text:
            return {'error':False, 'username':username, 'available':False, 'exists':True}
        return {'error':False, 'username':username, 'available':True, 'exists':False}
    except Exception as e:
        return {'error':e, 'username':username, 'available':None, 'exists':None}