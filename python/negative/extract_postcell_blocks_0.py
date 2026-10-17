
#negative have a better method below


def extract_postcell_blocks(html_or_soup):
    # negative... other similar methods seem better
    if html_or_soup is None:
        return []
    if isinstance(html_or_soup, str):
        soup = BeautifulSoup(html_or_soup, "html.parser")
    else:
        soup = html_or_soup
    mainbar = soup.select_one("div#mainbar[role='main'], div#mainbar")
    if not mainbar:
        return []
    blocks = []
    post_layouts = mainbar.find_all("div", class_=lambda x: x and "post-layout" in x)

    for post_layout in post_layouts:
        postcell = post_layout.find("div", class_=lambda x: x and "postcell" in x)
        if not postcell:
            continue

        prose = postcell.find("div", class_=lambda x: x and "s-prose" in x)
        if not prose:
            continue
        for child in prose.find_all(recursive=False):
            if child.name == "pre":
                code_block = extract_code_block(child)
                if code_block:
                    blocks.append(code_block)
            elif child.name in ["p","blockquote","ul","ol","h1","h2","h3","h4","h5","h6"]:
                text_block = extract_text_block(child)
                if text_block:
                    blocks.append(text_block)
    return blocks

