def extract_cve_cwe_ids_from_string_via_regex(text):
    """
    Extracts valid CWE and CVE IDs from the text.
    Returns list of dicts with line number, start/end positions, and matched text.
    """
    import re
    patterns = {
        'CVE': r'\bCVE-\d{4}-\d{4,}\b',
        'CWE': r'\bCWE-\d+\b'
    }
    matches = []
    lines = text.splitlines(keepends=True)
    char_offset = 0
    for line_num, line in enumerate(lines, start=1):
        for tag, pattern in patterns.items():
            for match in re.finditer(pattern, line, re.IGNORECASE):
                full_match = match.group()
                matches.append({
                    'type': tag,
                    'match': full_match,
                    'line': line_num,
                    'start': char_offset + match.start(),
                    'end': char_offset + match.end()
                })
        char_offset += len(line)

    return matches
#text = "This is a sample CVE-2023 report mentioning CVE-2024-1234 and CWE-79.\nBeware of invalid entries like CVE 2024-1234 or CWE79 or CVE:2024-1234."
#extract_cve_cwe_ids_from_string_via_regex(text)
# not working. the valid "CVE 2024-1234" and "CVE:2024-1234" was not extracted
#[{'type': 'CVE', 'match': 'CVE-2024-1234', 'line': 2, 'start': 45, 'end': 58},
# {'type': 'CWE', 'match': 'CWE-79', 'line': 2, 'start': 63, 'end': 69}]
