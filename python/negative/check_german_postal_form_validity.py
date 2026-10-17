def check_german_postal_form_validity(postcode:str|int='') -> str | None:
    try:
        if isinstance(postcode,(bytes, bytearray)):
            try:
                postcode = postcode.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    postcode = postcode.decode('latin1',errors='replace') # i replace here because we still catch for errors later if not isdigit for example
                except UnicodeDecodeError:
                    return None
        if not isinstance(postcode,(str,int)):
            return None
        if isinstance(postcode,(str,int)):
            postcode = f'{postcode}'.strip()
            if not postcode or not postcode.isdigit() or not  len(postcode) == 5:
                return None
            if int(postcode) not in range(1067,99999):
                return None
            return postcode    
        return None
    except Exception as ee:
        return None
