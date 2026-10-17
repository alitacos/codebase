def extract_structured_chunks_from_text_string_via_regex_and_ast(text : str = '') -> list :
    import re
    import ast
    chunks = []
    code_blocks = re.findall(
        r'```(?:\w+)?\s*(.*?)```',
        text,
        re.DOTALL
    )

    # ---------------------------------------------------------
    # 1. Triple-quoted strings: """...""" and '''...'''
    # ---------------------------------------------------------
    triple_pattern = re.compile(
        r'(?P<quote>"""|\'\'\')(.*?)(?P=quote)',
        re.DOTALL
    )

    for m in triple_pattern.finditer(text):
        chunks.append({
            "type": "triple_quote",
            "value": m.group(2),
            "quote": m.group("quote"),
            "start": m.start(),
            "end": m.end(),
        })

    # ---------------------------------------------------------
    # 2. HTML
    # ---------------------------------------------------------
    html_pattern = re.compile(
        r'<([A-Za-z][\w:-]*)(?:\s[^>]*)?>.*?</\1\s*>',
        re.DOTALL
    )

    for m in html_pattern.finditer(text):
        chunks.append({
            "type": "html",
            "value": m.group(0),
            "start": m.start(),
            "end": m.end(),
        })

    # ---------------------------------------------------------
    # 3. XML
    # ---------------------------------------------------------
    # XML looks similar to HTML, so this is intentionally
    # conservative. Actual XML parsing should use ElementTree.
    xml_pattern = re.compile(
        r'<([A-Za-z_][\w:.-]*)(?:\s[^>]*)?>.*?</\1\s*>',
        re.DOTALL
    )

    for m in xml_pattern.finditer(text):
        chunks.append({
            "type": "xml",
            "value": m.group(0),
            "start": m.start(),
            "end": m.end(),
        })

    # ---------------------------------------------------------
    # 4. Markdown tables
    # ---------------------------------------------------------
    lines = text.splitlines()
    table_lines = []
    i = 0

    while i < len(lines) - 1:
        # Header must contain |
        if "|" in lines[i]:
            # Next line should be markdown separator
            separator = lines[i + 1]

            if re.match(
                r'^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$',
                separator
            ):
                table = [lines[i], separator]
                i += 2

                while i < len(lines) and "|" in lines[i] and lines[i].strip():
                    table.append(lines[i])
                    i += 1

                chunks.append({
                    "type": "markdown_table",
                    "value": "\n".join(table),
                })

                continue

        i += 1

    # ---------------------------------------------------------
    # 5. Bold Markdown: **text** or __text__
    # ---------------------------------------------------------
    bold_pattern = re.compile(
        r'\*\*(.+?)\*\*|__(.+?)__',
        re.DOTALL
    )

    for m in bold_pattern.finditer(text):
        chunks.append({
            "type": "bold",
            "value": m.group(1) or m.group(2),
            "start": m.start(),
            "end": m.end(),
        })

    # ---------------------------------------------------------
    # 6. Italic Markdown: *text* or _text_
    # ---------------------------------------------------------
    italic_pattern = re.compile(
        r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)'
        r'|(?<!_)_(?!_)(.+?)(?<!_)_(?!_)',
        re.DOTALL
    )

    for m in italic_pattern.finditer(text):
        chunks.append({
            "type": "italic",
            "value": m.group(1) or m.group(2),
            "start": m.start(),
            "end": m.end(),
        })

    # ---------------------------------------------------------
    # Sort by position
    # ---------------------------------------------------------
    chunks.sort(key=lambda x: x.get("start", 0))

    return chunks
#example usage:
#extract_structured_chunks_from_text_string_via_regex_and_ast(text)