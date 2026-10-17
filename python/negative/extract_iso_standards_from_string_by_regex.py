def extract_iso_standards_from_string_by_regex(text):
    import re
    # is false positive
    pattern = r'\bISO(?:/IEC)?\s\d+(?::\d+)?\b'
    matches = []
    lines = text.splitlines()

    current_pos = 0
    for line_num, line in enumerate(lines, start=1):
        for match in re.finditer(pattern, line, re.IGNORECASE):
            matches.append({
                'match': match.group(),
                'line': line_num,
                'start': current_pos + match.start(),
                'end': current_pos + match.end()
            })
        current_pos += len(line) + 1  # +1 for newline

    return matches

 
# example usage :
#print("ISO Standards:", extract_iso_standards_from_string_by_regex('\nThis document references RFC-791 RFC - 791, RFC_7231 and ISO_27001 standards.\nAlso mentions ISO/IEC 27001:2013 and iso 9001.\n'))#out : ISO Standards: [{'match': 'ISO/IEC 27001:2013', 'line': 3, 'start': 93, 'end': 111}, {'match': 'iso 9001', 'line': 3, 'start': 116, 'end': 124}]
