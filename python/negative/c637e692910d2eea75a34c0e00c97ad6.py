def code(target):
    url=f"https://www.codecademy.com/{target}"
    inp = requests.get(f"{url}", headers={"user-agent": user_agent}).status_code
    if inp == 404:
        print(f" {ylw}[ {red}✖{ylw} ] {red}Code Academy Not Found")

    else:
        print(f" {ylw}[ {grn}✔{ylw} ] {grn}Code Academy Found: {url}")
        

        
