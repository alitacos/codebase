import requests

def check_username_in_weibo_if_exists_and_return_data_dict(username:str='',headers:dict=None, cookies:dict=None) -> dict:
    if not username:
        return {}

    session = requests.Session()

    

    try:
        url = f"https://m.weibo.cn/n/{username}"

        r = session.get(url, headers=headers, allow_redirects=True)

        print("first url:", r.url)

        # visitor redirect
        if "visitor.passport.weibo.cn" in r.url:
            visitor = session.get(r.url, headers=headers)
            print("visitor:", visitor.status_code)

            r = session.get(
                url,
                headers=headers,
                allow_redirects=True
            )

        print("final url:", r.url)

        if "/u/" in r.url:
            uid = r.url.split("/u/")[1].split("?")[0]

            api = f"https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}"

            api_response = session.get(api, headers={
                **headers,
                "Accept": "application/json, text/plain, */*",
                "X-Requested-With": "XMLHttpRequest"
            })

            return api_response.json()

        return {
            "ok": 0,
            "msg": "这里还没有内容",
            "data": {"cards": []}
        }

    except Exception as e:
        return {
            "ok": 0,
            "msg": str(e),
            "data": {"cards": []}
        }

