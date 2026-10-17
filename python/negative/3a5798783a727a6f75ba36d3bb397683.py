def cash(target):
    url=f"https://cash.me/{target}"
    inp = requests.get(f"{url}").status_code
    if inp == 404:
        print(f" {ylw}[ {red}✖{ylw} ] {red}Cash Me Not Found")

    else:
        print(f" {ylw}[ {grn}✔{ylw} ] {grn}Cash Me Found: {url}")
