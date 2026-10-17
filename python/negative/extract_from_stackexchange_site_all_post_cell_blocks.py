def extract_from_stackexchange_site_all_post_cell_blocks(url:str='')->dict:    
    import bs4
    from bs4 import BeautifulSoup
    import html
    
    # ----------------------------
    # LANGUAGE DETECTION
    # ----------------------------
    def detect_language(pre_tag, code_tag):
        # 1. From <pre class="lang-r ...">
        lang_=None
        for c in pre_tag.get("class", []):
            if c.startswith("lang-"):
                lang_= c.replace("lang-", "")
    
        # 2. From <code class="language-r ...">
        for c in code_tag.get("class", []):
            if "language-" in c:
                lang_= c.split("language-")[-1]
    
        # 3. Heuristic fallback from code content
        text = code_tag.get_text().strip()
        if not lang_ and  text.startswith(">") or "as.matrix" in text or "read.table" in text:
            lang_= "r"
        if not lang_ and "def " in text or "import " in text:
            lang_= "python"
        if not lang_ and "SELECT" in text.upper():
            lang_= "sql"
        if lang_ and lang_=='py':
            return 'python'
        if lang_ and lang_=='js':
            return 'javascript'
        return lang_ if lang_ else ""
    
    # ----------------------------
    # CODE BLOCK HANDLING
    def convert_to_markdown(element)->str:
        from html_to_markdown import convert
        result = convert(element)
        return result
    def extract_code_block(pre_tag):
    
    
        if not pre_tag or pre_tag.name != "pre":
            return None
    
        code_tag = pre_tag.find("code")
        if not code_tag:
            return None
    
        lang = detect_language(pre_tag, code_tag)
        lang = lang if lang and lang.strip() and lang not in [None,'None','none'] else ""
        code_text = html.unescape(code_tag.get_text("\n")).strip()
        if code_text:
            return {
            "type": "code",
            "language": lang ,
            "html_string": str(pre_tag),#{lang}
            "markdown": f"""```
            {convert_to_markdown(str(pre_tag)).content}
            ```""",
    
            "metadata": f"""{convert_to_markdown(str(pre_tag)).metadata}""",
            "markdown_lines": len(code_text.splitlines()) + 2,
            "markdown_size": len(code_text)
        }
        return None
    # ----------------------------
    # TEXT / LATEX / HEADINGS / LINKS
    # ----------------------------
    def extract_text_block(tag: bs4.element.Tag):
        text = tag.get_text("\n").strip()
        if not text:
            return None
    
        # --- LaTeX detection ---
        if ":math:" in text or r"\\frac" in text:
            return {
                "type": "latex",
                "language": "latex",
                "html_string": str(tag),#{lang}
                "markdown": f"""```
                {convert_to_markdown(str(tag)).content}
                ```""",
                "metadata": f"""{convert_to_markdown(str(tag)).metadata}""",
    
                "markdown_lines": len(text.splitlines()),
                "markdown_size": len(text)
            }
    
        # --- heading support ---
        if tag.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            level = int(tag.name[1])
            text = ("#" * level) + " " + text
    
        # --- link rewriting ---
        for a in tag.find_all("a"):
            href = a.get("href", "")
            label = a.get_text()
            if href:
                text = text.replace(label, f"[{label}]({href})")
    
        return {
            "type": "text",
            "language": "en",# How to verify additionally?
            "html_string": str(tag) if tag else "",
            "markdown": f"""
            {convert_to_markdown(str(tag) if tag else "").content}
            """,
            "metadata": f"""{convert_to_markdown(str(tag) if tag else "").metadata}""",
            "markdown_lines": len(text.splitlines()),
            "markdown_size": len(text)
        }
    
    
    def self_retrieve_record_source(url='https://stackoverflow.com/questions/22255159/how-to-convert-str-to-int', lastTimeLimitError: str   = '', timeout=5) -> dict:
        import requests
        import bs4
        try:
            return bs4.BeautifulSoup(requests.get(url , timeout=timeout).text)
        except:
            return None
    
    def extract_postcell_blocks_from_stackexchange_questions_page(html_or_soup):
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
       # print(convert_to_markdown(post_layouts[0].get_text()).content)
        for post_layout in post_layouts:
            postcell = post_layout.find("div", class_=lambda x: x and "postcell" in x)
            if not postcell:
                continue
    
            prose = postcell.find("div", class_=lambda x: x and "s-prose" in x)
            if not prose:
                continue
    
            # iterate only **top-level block elements** inside prose
            for child in prose.contents:#find_all(recursive=False):
                if child.name in ["script", "style"]:
                    continue
    
                if child.name == "pre":
                    code_block = extract_code_block(child)
                    if code_block and code_block.get('markdown','').strip() :
                        blocks.append(code_block)
                    continue
    
                # for everything else, treat as a text block
                text_block = extract_text_block(child)
                if text_block and text_block.get('markdown','').strip() :
                    blocks.append(text_block)
                    continue
        return blocks
    soup = self_retrieve_record_source(url=url)
    return  extract_postcell_blocks_from_stackexchange_questions_page(soup )
# nothing happened  . i get text of soup  '''Just a moment...''' and text ''''Just a moment...Enable JavaScript and cookies to continue''''