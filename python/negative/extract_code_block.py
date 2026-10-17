
def extract_code_block(pre_tag):
    if not pre_tag or pre_tag.name != "pre":
        return None
    code_tag = pre_tag.find("code")
    if not code_tag:
        return None
    lang = detect_language(pre_tag, code_tag)
    code_text = html.unescape(code_tag.get_text("\n"))
    return { "type": "code", "language": lang, "html_string": str(pre_tag), "markdown": f"```{lang}\n{code_text}\n```", "markdown_lines": len(code_text.splitlines()) + 2, "markdown_size": len(code_text) }
