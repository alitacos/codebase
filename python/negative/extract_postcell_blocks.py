# negatives, or low quality or untested
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
    post_layouts = mainbar.find_all( "div", class_=lambda x: x and "post-layout" in x )
    for post_layout in post_layouts:
        # find the right postcell
        postcell = post_layout.find( "div", class_=lambda x: x and "postcell" in x )
        if not postcell:
            continue
        prose = postcell.find( "div", class_=lambda x: x and "s-prose" in x )
        if not prose:
            continue
        for child in prose.children:
            if isinstance(child, str):
                continue
            if   isinstance(child, bs4.element.Tag):
                continue
            if child.name in ["script", "style"]:
                continue
            if child.name == "pre":
                continue
    return blocks


