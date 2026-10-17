#KeyError: 'key'
def check_german_federal_state_data(region_input: str | int='') -> list:
    """
    Check if region_input matches a German federal state (by key, short name, or full name).
    If yes, call the ladies.de API with the full name as searchString.

    Args:
        region_input (str|int): Name, shortcode, or numeric key of federal state.

    Returns:
        dict | None: JSON response or None if invalid input or request failure.
    """
    import requests
    federal_states = [{'ags': '01', 'name': 'Schleswig-Holstein', 'short': 'SH', 'iso-3166-2': 'DE-SH'}, {'ags': '02', 'name': 'Hamburg', 'short': 'HH', 'iso-3166-2': 'DE-HH'}, {'ags': '03', 'name': 'Niedersachsen', 'short': 'NI', 'iso-3166-2': 'DE-NI'}, {'ags': '04', 'name': 'Bremen', 'short': 'HB', 'iso-3166-2': 'DE-HB'}, {'ags': '05', 'name': 'Nordrhein-Westfalen', 'short': 'NW', 'iso-3166-2': 'DE-NW'}, {'ags': '06', 'name': 'Hessen', 'short': 'HE', 'iso-3166-2': 'DE-HE'}, {'ags': '07', 'name': 'Rheinland-Pfalz', 'short': 'RP', 'iso-3166-2': 'DE-RP'}, {'ags': '08', 'name': 'Baden-Württemberg', 'short': 'BW', 'iso-3166-2': 'DE-BW'}, {'ags': '09', 'name': 'Bayern', 'short': 'BY', 'iso-3166-2': 'DE-BY'}, {'ags': '10', 'name': 'Saarland', 'short': 'SL', 'iso-3166-2': 'DE-SL'}, {'ags': '11', 'name': 'Berlin', 'short': 'BE', 'iso-3166-2': 'DE-BE'}, {'ags': '12', 'name': 'Brandenburg', 'short': 'BB', 'iso-3166-2': 'DE-BB'}, {'ags': '13', 'name': 'Mecklenburg-Vorpommern', 'short': 'MV', 'iso-3166-2': 'DE-MV'}, {'ags': '14', 'name': 'Sachsen', 'short': 'SN', 'iso-3166-2': 'DE-SN'}, {'ags': '15', 'name': 'Sachsen-Anhalt', 'short': 'ST', 'iso-3166-2': 'DE-ST'}, {'ags': '16', 'name': 'Thüringen', 'short': 'TH', 'iso-3166-2': 'DE-TH'}]

    def normalize(text: str) -> str:
        return text.lower().replace('ü', 'ue').replace('ä', 'ae').replace('ö', 'oe').replace('ß', 'ss').strip()
    if isinstance(region_input, int):
        user_input = f'{region_input:02d}'
    else:
        user_input = normalize(str(region_input))
    matched_state = None
    for state in federal_states:
        key = state['key']
        name = normalize(state['name'])
        short = state['short'].lower()
        if user_input == key or user_input == key.lstrip('0') or user_input == name or (user_input == short):
            matched_state = state
            break
    if not matched_state:
        print(f"Input '{region_input}' is not a recognized German federal state.")
        return None
    url = 'https://www.ladies.de/api/location/'
    params = {'searchString': matched_state['name'], 'searchAddAlleRegionen': 'false'}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Request failed: {e}')
        return None
