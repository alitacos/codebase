def check_german_kfz_code_per_localities_state_and_postalcode(localities: list=[], federalstate: str='', postalcode: str=''):
    """
    Searches for a German KFZ (vehicle registration) code based on locality name(s),
    federal state, and optional postal code by matching against a local KFZ dataset.
    
    The function normalizes and cleans input locality names, then attempts to find
    matching entries in a dataset of German vehicle registration identifiers. It first
    tries exact matching and then falls back to prefix matching if no exact match is found.
    
    Args:
        localities (list): List of city or district names to search for KFZ codes.
        federalstate (str): Full name of the German federal state (e.g. "Bayern").
        postalcode (str): Optional postal code used to refine locality name matching.
    
    Returns:
        Any: KFZ object containing:
            - code: matched KFZ registration code (Unterscheidungszeichen)
            - city: matched locality name
            - error: error message if lookup fails or no match is found
    
    Example usage:
        >>> result = check_german_kfz_code_per_localities_state_and_postalcode(  localities=['Augsburg'],  federalstate='Bayern', postalcode='86150')
    """
    import csv, unicodedata, re

    class KFZ:

        def __init__(self, code: str='', city: str='', error: dict=None):
            self.code: str = code.strip() if code and isinstance(code, str) else None
            self.city: str = city.strip() if city and isinstance(city, str) else None
            self.type: str = 'kfz_code'
            self.error: str = error if error else None

    kfz_dataset = get_german_kfc_data_dict()

    def normalize(s: str) -> str:
        s = str(s).lower().strip()
        s = ''.join((c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c)))
        s = re.sub('[^a-z0-9]', '', s)
        return s

    def clean_name(name: str='', postalcode: str='') -> str:
        suffixes = [', Stadtkreis', ', Landeshauptstadt', ', Kreisfreie Stadt', ', kreisfreie Stadt', ', Stadt', ' (Stadtkreis)', ' (Landeshauptstadt)', ' (Kreisfreie Stadt)', ' (kreisfreie Stadt)', ', stadtkreis', ', landeshauptstadt', ', kreisfreie stadt', ', stadt', ' (stadtkreis)', ' (landeshauptstadt)', ' (kreisfreie stadt)']
        if postalcode:
            suffixes.extend([f'{postalcode}', f'({postalcode})'])
        name = name.strip() if name and isinstance(name, str) else ''
        for s in suffixes:
            if name.endswith(s):
                name = name[:-len(s)].strip()
        return name
    if not localities:
        return KFZ(code=None, city=None, error='Invalid input. Missing <localities>  ')
    if not federalstate:
        return KFZ(code=None, city=None, error='Invalid input. Missing <federalstate>  ')
    try:
        rows = []
        lacales = []
        for name in localities:
            if not name:
                continue
            lookup = normalize(clean_name(name=name, postalcode=postalcode))
            _rows = [r for r in kfz_dataset if normalize(r['StadtOderKreis']) == lookup and r['Bundesland.Name'] == federalstate]
            if _rows:
                rows.extend(_rows)
                break
        if not rows:
            for name in localities:
                if not name:
                    continue
                lookup = normalize(clean_name(name=name, postalcode=postalcode))
                _rows = [r for r in kfz_dataset if normalize(r['StadtOderKreis']).startswith(normalize(lookup)) and r['Bundesland.Name'] == federalstate]
                if _rows:
                    rows.extend(_rows)
        if rows:
            kfz = rows[0]['Unterscheidungszeichen']
            if kfz:
                return KFZ(code=kfz, city=lookup, error=None)
        return KFZ(code=None, city=None, error='Invalid input. No kfz_code found')
    except Exception as e:
        return KFZ(code=None, city=None, error=e)