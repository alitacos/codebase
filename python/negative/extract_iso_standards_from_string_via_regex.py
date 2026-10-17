def extract_iso_standards_from_string_via_regex(text):
    # not working for all patterns like 'ISO_9898' or 'iso-9002'
    import re
    pattern = r'\bISO(?:/IEC)?\s\d+(?::\d+)?\b'
    matches = []
    lines = text.splitlines(keepends=True)
    char_offset = 0

    for line_num, line in enumerate(lines, start=1):
        for match in re.finditer(pattern, line, re.IGNORECASE):
            matches.append({
                'match': match.group(),
                'line': line_num,
                'start': char_offset + match.start(),
                'end': char_offset + match.end()
            })
        char_offset += len(line)

    return matches
#example usage :
#extract_iso_standards_from_string_via_regex('hallo iso 9001 and ISO_9898 or iso-9002')
