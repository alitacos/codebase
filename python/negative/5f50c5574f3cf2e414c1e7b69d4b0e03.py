def paste(target):
    url=f"https://pastebin.com/u/{target}"
    inp = requests.get(f"{url}", headers={"user-agent": user_agent}).status_code
    if inp == 404:
        print(f" {ylw}[ {red}✖{ylw} ] {red}Pastebin Not Found")

    else:
        print(f" {ylw}[ {grn}✔{ylw} ] {grn}Pastebin Found: {url}")
        

        

        
