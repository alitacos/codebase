def check_password_validity_for_github_accounts( password: str='',token:str='', cookies:dict=None,headers:dict=None,hide_password_validity_pills:bool=True,hide_strength_sentence:bool=True)->dict:
    import requests
    from bs4 import BeautifulSoup
    if hide_strength_sentence:
        strength_sentence = 'true'
    else:
        strength_sentence = 'false'
    if hide_password_validity_pills:
        validity_pills = 'true'
    else:
        validity_pills ='false'

        
    url = f'https://github.com/password_validity_checks?hide_password_validity_pills={validity_pills}&hide_strength_sentence={strength_sentence}'
    if not token:
        token = 'Xq1hAnWbMXu66YV4MTMdeIZXNlxYLpXih2BCX6njBt74xQaW+F1wGXYeQrJFLlSxwD78Fl9bIs6OrAUWaqo1gg=='
    payload = {
        "hide_password_validity_pills":validity_pills,
        "hide_strength_sentence":strength_sentence,
        "authenticity_token":token,
        "value": password
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
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    # Note: For multipart form data, requests can set the boundary automatically,
    # so omit Content-Type or use 'multipart/form-data' without boundary manually.
    # But if you want to specify it, do it carefully.
    # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary1qT9AFWO3UPZprG0",
    "Origin": "https://github.com",
    "Referer": "https://github.com/signup?return_to=https%3A%2F%2Fgithub.com%2Flogin&source=login",
    "Sec-CH-UA": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Priority": "u=1, i"
}



    response = requests.post(url, params=payload,cookies=cookies)

    try:
        return  {
            "error": None,
            "status_code": response.status_code,
            "text": '\n'.join([i.strip() for i in BeautifulSoup(response.text,'html.parser').text.strip().splitlines() if i.strip()])
        }
        
 
    except Exception as e:
        return {
            "error": str(e),
            "status_code": response.status_code,
            "text": response.text
        }
#example usage:
 
#check_password_validity_for_github_accounts(password='xxxmag0sxxx')#Password is strong
#check_password_validity_for_github_accounts(password='a')#Password is too short
#check_password_validity_for_github_accounts(password='33333333333333333')#Password may be compromised\nPassword is in a list of passwords commonly used on other websites
#check_password_validity_for_github_accounts(password='xxxmag')#Password is too short
