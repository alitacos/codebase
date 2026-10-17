def xbox(target):
    url=f"https://playerdb.co/api/player/xbox/{target}"
    inp = requests.get(f"{url}", headers={"user-agent": user_agent}).status_code
    if inp != 200:
        print(f" {ylw}[ {red}✖{ylw} ] {red}Xbox Not Found")

    else:
        print(f" {ylw}[ {grn}✔{ylw} ] {grn}Xbox Found: {url}")



        

        

        
