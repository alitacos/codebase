def extract_text_block_from_html_element(tag: bs4.element.Tag) - > dict :
    text = tag.get_text("\n").strip()
    if not text:
        return None
    if ":math:" in text or r"\\frac" in text:
        return { "type": "latex", "language": "latex", "html_string": str(tag), "markdown": f"""``` {convert_to_markdown(str(tag)).content} ```""", "metadata": f"""{convert_to_markdown(str(tag)).metadata}""", "markdown_lines": len(text.splitlines()), "markdown_size": len(text) }
    if tag.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        level = int(tag.name[1])
        text = ("#" * level) + " " + text
    for a in tag.find_all("a"):
        href = a.get("href", "")
        label = a.get_text()
        if href:
            text = text.replace(label, f"[{label}]({href})")
    return { "type": "text", "language": "en", "html_string": str(tag) if tag else "", "markdown": f""" {convert_to_markdown(str(tag) if tag else "").content} """, "metadata": f"""{convert_to_markdown(str(tag) if tag else "").metadata}""", "markdown_lines": len(text.splitlines()), "markdown_size": len(text) }
