# negatives, or low quality or untested

def extract_text_block(tag: bs4.element.Tag):
    # negative : have a better method tht also handles latex
    if tag is None:
        return None
    text = tag.get_text(" ", strip=True)
    if not text:
        return None
    if tag.name in ["h1","h2","h3","h4","h5","h6"]:
        level = int(tag.name[1])
        text = ("#" * level) + " " + text
    for a in tag.find_all("a"):
        href = a.get("href","")
        label = a.get_text()
        if href:
            text = text.replace(label, f"[{label}]({href})")
    return { "type": "text", "language": "en", "html_string": str(tag), "markdown": text, "markdown_lines": len(text.splitlines()), "markdown_size": len(text) }
