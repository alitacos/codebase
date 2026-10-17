def extract_rfc_numbers_from_string_via_regex(text):
    import re
    # NOT WORKING
    # Match 'RFC 1234' or 'RFC-1234' with 1 to 4 digits and total length 8
    pattern = r'\bRFC(\s?:-\s?|\s?)\d{1,4}\b'  # Allow exactly one space or one dash
    matches = []
    lines = text.splitlines(keepends=True)
    char_offset = 0
    for line_num, line in enumerate(lines, start=1):
        for match in re.finditer(pattern, line, re.IGNORECASE):
            full_match = match.group()
            if len(full_match) <= 10:
                matches.append({
                    'match': full_match,
                    'line': line_num,
                    'start': char_offset + match.start(),
                    'end': char_offset + match.end()
                })
        char_offset += len(line)
    return matches
#EXAMPLE USAGE :
#extract_rfc_numbers_from_string_via_regex('\nThis document references RFC 791, RFC - 7231 and ISO 27001 standards.\nAlso mentions ISO/IEC 27001:2013 and iso 9001 or RFC-7231.\n')
