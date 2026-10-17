def check_username_in_weibo_if_exists_and_return_data_dict(username:str='',headers:dict=None, cookies:dict=None) -> dict:
    if not username:
        return {}
    import requests
    from bs4 import BeautifulSoup
    url = f'https://m.weibo.cn/n/{username}'
    if not headers:
        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Referer": "https://m.weibo.cn/" }
    
    if not cookies:
        cookies = { "_T_WM": "68692310357", "M_WEIBOCN_PARAMS": "luicode%3D10000011%26lfid%3D1076031847337503%26fid%3D1005051847337503%26uicode%3D10000011", "MLOGIN": "0", "SUB": "_2AkMdCL5gf8NxqwFRnP4VyG_gbIV-ygvEieKrVE-7JRM3HRl-yT9yqmc7tRB6NoiQj8sXLC8C_x9lDumU3e3XGGt2YhCA", "SUBP": "0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhJ1Q605n.XVQY_A3hVsVUl", "WEIBOCN_FROM": "1110006030", "XSRF-TOKEN": "9dcf69" }
    r = requests.get(url,headers=headers,cookies=cookies)
    if r.status_code == 200:
        if 'https://m.weibo.cn/n/' in r.url:  
            try:
                soup = BeautifulSoup(r.content,'html.parser').find('p',{"class":"h5-4con"}).text
                print(soup)
                if soup in ['啊哦，你要找的页面不见啦！','这里还没有内容','用户不存在','该昵称当前没有人使用。']:
                    #print(str('h5-4con'))
                    return {'ok': 0, 'msg': '这里还没有内容', 'data': {'cards': []}}

            except Exception as e1:
                print(str(e1))
                return {'ok': 0, 'msg': '这里还没有内容', 'data': {'cards': []}}

        if 'https://m.weibo.cn/u/' in r.url: 
            uiid = r.url.replace('https://m.weibo.cn/u/','').strip()
            link =f'https://m.weibo.cn/api/container/getIndex?type=uid&value={uiid}'
            r = requests.get(link)
            try:
                return r.json()#find_all('div',{"class":"item-list"})
            except Exception:
                soup = BeautifulSoup(r.content,'html.parser').find('div',{"class":"empty_failed"}).text  
                if soup in ['啊哦，你要找的页面不见啦！','这里还没有内容','用户不存在','该昵称当前没有人使用。']:
                    #print('empty_failed')
                    return {'ok': 0, 'msg': '这里还没有内容', 'data': {'cards': []}}

    return {'ok': 0, 'msg': '这里还没有内容', 'data': {'cards': []}}