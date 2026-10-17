def check_if_email_exists_in_snapchat(email:str=None, cookies:dict={},headers:dict={},payload:dict={} ):
    #requires javascript -> selenium
    import requests

    url="https://accounts.snapchat.com/accounts/v2/login"

    payload ={'accountIdentifier': str(email).strip() if email else None,
 'xsrf_token': 'j1pcmapFTnsML5OjpzhCfw',
 'continue': '/accounts/welcome',
 'captcha-payload': 'CAES8AIzMjUxODRhMDQ2ODQ4ZTA2Mi45NjI5MDgwMjA1fHI9ZXUtd2VzdC0xfG1ldGE9M3xtZXRhYmdjbHI9dHJhbnNwYXJlbnR8bWV0YWljb25jbHI9JTIzNzU3NTc1fGd1aXRleHRjb2xvcj0lMjMwMDAwMDB8bGFuZz1kZXxwaz0wN0VBQjRCOC0yRDgwLTQyMzQtQjg5Ny1BMkNEMUYxOTQ4NjZ8YXQ9NDB8c3VwPTF8cmlkPTM1fGFnPTEwMXxjZG5fdXJsPWh0dHBzJTNBJTJGJTJGc25hcC1hcGkuYXJrb3NlbGFicy5jb20lMkZjZG4lMkZmY3xzdXJsPWh0dHBzJTNBJTJGJTJGc25hcC1hcGkuYXJrb3NlbGFicy5jb218c211cmw9aHR0cHMlM0ElMkYlMkZzbmFwLWFwaS5hcmtvc2VsYWJzLmNvbSUyRmNkbiUyRmZjJTJGYXNzZXRzJTJGc3R5bGUtbWFuYWdlcg==',
 'attestation': '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',
 'accountIdentifierCountryCode': ''}
 

# Cookies dictionary
    cookies = {
    'xsrf_token': 'xsrf_token=F3pvkY5HqpxnoCL00yE2-g; sc-wcid=efa4b0c8-82ed-430f-aee6-2ac2faf38767; _sc-sid=da9616b4-dfd9-44f5-b684-97fe75fb215b; sc-cookies-accepted=true; EssentialSession=true; Preferences=false; Performance=false; Marketing=false; __Host-X-Snap-Client-Cookie=CAISOsN4T4e5a0A0IILnhkYj3Fupjr+reZyoupieZkAZIoPoYQqBq7scOhDQHWb54Txtwe0LmfQQst6hKzE; __Host-sc-authn-session-payload=Cg0xNzUwMjA4MDI4NjY1EmFqkW58nWTG7F7_j7KCwd2HzVzrCtbHQwIkCrfeRovSceSkTx-qWxk6_OA-ODagcNV5uUh26YSSbk3HpgABTqmtEeoB-_kg6qhzELFTDiybvTIr7mLgP7sdt6bhu4Qo0UN7GgziPx7DB0VXC81WNQM=',
    'sc-wcid': 'efa4b0c8-82ed-430f-aee6-2ac2faf38767',
    '_sc-sid': 'da9616b4-dfd9-44f5-b684-97fe75fb215b',
    'sc-cookies-accepted': 'true',
    'EssentialSession': 'true',
    'Preferences': 'false',
    'Performance': 'false',
    'Marketing': 'false',
}

# Headers dictionary
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'referer': 'https://accounts.snapchat.com/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',  # Add this if posting form data
}


 
    
    response= requests.post(url, cookies=cookies,headers=headers, data=payload)# 
    return response
res= check_if_email_exists_in_snapchat(email='anon@grr.la')
 #res.headers['Content-Type'] -> 'text/html'
# i verified above but still i get error and then moves to json
try:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(res.content, 'html.parser')
    div = soup.find('div', {'id': 'account-identifier-root'})
    
    data_error = div.get('data-error') if div else None
    data_ai_token = div.get('data-ai-token') if div else None
    data_xsrf = div.get('data-xsrf') if div else None

    print("data-error:", data_error)
    print("data-ai-token:", data_ai_token)
    print("data-xsrf:", data_xsrf)
    #CONCLUSION==> not working....requires selenium

except Exception as e:
    print(str(e))
    print(res.json())   
