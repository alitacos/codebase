def wiki(target):
    url=f"https://www.wikipedia.org/wiki/User:{target}"
    inp = requests.get(f"{url}", headers={"user-agent": user_agent}).status_code
    if inp == 404:
        print(f" {ylw}[ {red}✖{ylw} ] {red}Wikipedia Not Found")

    else:
        print(f" {ylw}[ {grn}✔{ylw} ] {grn}Wikipedia Found: {url}")


        

        

        
