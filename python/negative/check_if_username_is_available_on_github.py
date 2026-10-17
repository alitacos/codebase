def check_if_username_is_available_on_github( username: str='',cookies:dict=None,headers:dict=None)->dict:
    import requests
    from bs4 import BeautifulSoup

    url = f'https://github.com/signup_check/username?value={username}'
    
    payload = {
         
        'value': username
    }
    if not cookies:
        cookies = {
    "_octo": "GH1.1.2001113065.1749663192",
    "logged_in": "no",
    "cpu_bucket": "xlg",
    "preferred_color_mode": "dark",
    "tz": "Europe%2FBerlin",
    "_device_id": "dcb166d6b9cca808ca835b31228f994c",
    "GHCC": "Required:1-Analytics:0-SocialMedia:0-Advertising:0",
    "_gh_sess": "V5pRY9s0eyXsUFIQ2eD4yb3Wm8fvMLzdcs8WwpFPpb8LgsgrqkvpHjBx3Bxh7%2BpdjXUEYg2jb9Spw3PNP4N7sZdArMrEVzFhwhWsta%2FDfChQ5nvkOWbQ2V0V91wxy989CKJxPwckMPA3AXM7btTDWYnbJnA7UpYJZ7zwjNaReoSKXyVv2KGzWloVlHnp%2F3h%2FbHlqA3Zjin1BmbtTqIggTr6msmvIEM8W%2FkMwq1NFwLEyEkLeyffc5ceGm4l32Ivh5kW8aeTOl4kj5EOsKHLMGkklyQBBRjE2YT5XPDm70DpetSU%2F%2FwtmkZUbdPSyWhbSrS9Goq3uYpVPvXge%2BP2w55enueGxoio9jbk6gsDty3A5MuwkbDTI1VW88iBvoQZs7akQAq4wu0UMgJLtQWh6%2F9JrXAKFXmw%2Bd48UK6CKsOdjNLAZCOWny%2B8jQDTO4MBZBi2IX67rr05iyWcLPiAG6YUjkG5VzCk2sHUIhwj7gty2o6wWUeL9L62mj730tlGF0Td%2Fv%2FyxfnTrBDhESiB%2F2AeGMvaT%2Bqhva22tgEYytmaaiyBSooXA8Do4dGveUcXDB6s2JxImR4ocPg79LnftdYkrSBSJERM60vCu3fyk1YMA0p8m9g2DpswQWeRd3ZWcewpO1s1F711mjYEY%2FQxSMSZCAmMdpvZvbyuwcKdEPrd4xAzIOtnnHgad%2BDK%2FaRN3XxfIXHQRn%2BjOG0404czq6lzqJ%2FrdFKjmwRamb1zSfJura2v4vMyk2rlAc1cat5N4w3XzYURs6FRKvPk4J2iDpQ%3D%3D--iQdDBAee9l15%2B9%2Bn--DwDVgDCpqT6PCkSpYWNhqQ%3D%3D"
}

    if not headers:
        headers = {
    "Accept": "*/*",
    "Referer": "https://github.com/signup?return_to=https%3A%2F%2Fgithub.com%2Flogin&source=login",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-CH-UA": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Windows\""
}


    response = requests.get(url, params=payload,cookies=cookies)

    try:
        return  {
            "error": None,
            "status_code": response.status_code,
            "message": ' '.join(BeautifulSoup(response.text,'html.parser').text.strip().split()),
            'available': False if 'is not available' in ' '.join(BeautifulSoup(response.text,'html.parser').text.strip().split()) else True
        }
        
 
    except Exception as e:
        return {
            "error": str(e),
            "status_code": response.status_code,
            "message": ' '.join(response.text.strip().split()),
            'available':False
        }
#example usage:
#check_if_username_is_available_on_github(username='anonymous')