# would not work without the expected imports. 
def detect_country_info_from_mobile_phone_num(number: str='') -> dict:
    """
    Detect country info from a given phone number.

    Args:
        number (str): Phone number in any format.

    Returns:
        dict: Country info dictionary if matched; empty dict otherwise.
    """
    import re
    try:
        number = normalize_phone_number(number)
        if number.startswith('00'):
            number = '+' + number[2:]
        if not number.startswith('+'):
            return {}
        countries = phone_country_codes()

        def is_valid_operator(number: str, operators: list) -> bool:
            for op in operators:
                prefix = op.get('prefix')
                infix = op.get('infix')
                lengths = op.get('length', [])
                full_prefix = prefix + infix
                if number.startswith(full_prefix) and len(number[len(prefix):]) in lengths:
                    return True
            return False
        if number.startswith('+49') and is_valid_operator(number, german_mobile_operators()):
            for c in countries:
                if c.get('country_code') == 'DE' or c.get('prefix') == '+49':
                    return c
        if number.startswith('+30') and is_valid_operator(number, greek_mobile_operators()):
            for c in countries:
                if c.get('country_code') == 'GR' or c.get('prefix') == '+30':
                    return c
        if number.startswith('+31') and is_valid_operator(number, dutch_mobile_operators()):
            for c in countries:
                if c.get('country_code') == 'NL' or c.get('prefix') == '+31':
                    return c
        for c in sorted(countries, key=lambda x: -len(x.get('prefix', ''))):
            prefix = c.get('prefix', '')
            if number.startswith(prefix):
                return c
        return {}
    except Exception:
        return {}