import httpx
import asyncio
import json
import requests

async def check_if_account_exists_on_pinterest_via_async(email: str='',verbose:bool=False,csrftoken:str='',cookie:str='',lang:str='de',show:bool=False,print_response:bool=False)-> bool:
    # requires some optimization and checking
    url = "https://de.pinterest.com/resource/ApiResource/create/"
    if csrftoken:
        csrftoken = str(csrftoken)
    else:
        csrftoken = '<your_csrf_token>'
    if cookie:
        cookie = str(cookie)
    else:
        cookie = '<your_session_cookie>'
    if not email:
        if verbose:
            print('<email> input is missing. Pplease add a valid email string')
        return False
    if email:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.92 Safari/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.pinterest.com/",
                "Origin": f"https://{lang}.pinterest.com"  if lang else 'en',
                # You can set these cookies manually or extract them from your browser session
                "Cookie": f"csrftoken={csrftoken}; _pinterest_sess={str(cookie)};" ,
                "x-csrftoken": f"{csrftoken}",}
            payload = {"source_url": "/","data": json.dumps({"options": {"url": "/v3/sso/info/", "data": {"email": email}, },"context": {} })}
            async with httpx.AsyncClient(follow_redirects=True) as client:  # Ensure redirects are followed
                response = await client.post(url, headers=headers, data=payload)
                if verbose:
                    print("Status code:", response.status_code)
                    if print_response:
                        print("Response text:", response.content)  # Show first part of the body
                if response.status_code == 302:
                    # Handle the redirect manually if necessary
                    redirect_url = response.headers.get('Location')
                    if verbose:
                        print(f"Redirected to: {redirect_url}")
                    # You may need to make another request to the redirected URL
                else:
                    try:
                        json_data = response.json()
                        if show:
                            print(json_data)
                        exists = 0  # Modify based on the actual response structure
                        if exists:
                            return True
                        else:
                            return False
                    except Exception as e:
                        if verbose:
                            print(f"\033[91m>\033[0m Pinterest: failed to parse JSON ({e})")
                        return False
        except Exception as r:
            if verbose:
                print(str(r))
            return False
# example usage in Jupyter or notebook:
#await check_if_account_exists_on_pinterest_via_async(email="alitakos29@gmail.com")
# so it is not working. should retur True, but returns False