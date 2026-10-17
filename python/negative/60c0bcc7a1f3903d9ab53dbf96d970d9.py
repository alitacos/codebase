def count_of_enclosing_symbols_in_text_via_regex(text: str=''):
    import re
    return len(re.findall('[\\(\\)\\[\\]\\{\\}\\>\\<]', text))