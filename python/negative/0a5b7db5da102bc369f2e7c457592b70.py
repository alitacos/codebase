def check_if_email_exists_on_pinterest_via_requests_and_related_data_in_dict(email: str = '', verbose: bool = False) -> dict:
    """
    Check whether an email address appears to exist on Pinterest by querying a public endpoint and interpreting the response.
    
    Args:
        email (str): Email address to check.
        verbose (bool): If True, prints debug information such as status code
                        and partial response.
    Returns:
        dict: Parsed response dictionary with additional keys:
              - available: True if email is not registered
              - taken: True if email is already registered
              Returns False on failure.
    Example usage:
        result = check_if_email_exists_on_pinterest_via_requests_and_related_data_in_dict(email="test@example.com", verbose=False)
    """
    import requests
    import json
    if not email:
        if verbose:
            print('<email> argument is missing. Please add a valid string in input')
        return False
    try:
        source_url = '/password/reset/'
        data_payload = {'options': {'url': '/v3/register/exists/', 'data': {'email': email}}, 'context': {}}
        query_params = {'source_url': source_url, 'data': json.dumps(data_payload), '_': '1750075105176'}
        base_url = 'https://de.pinterest.com/resource/ApiResource/get/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Referer': 'https://de.pinterest.com/', 'X-Requested-With': 'XMLHttpRequest', 'X-Pinterest-AppState': 'active', 'X-Pinterest-PWS-Handler': 'www/password/reset.js', 'X-Pinterest-Source-Url': source_url, 'X-App-Version': 'd8c18cb'}
        cookies = {'csrftoken': '0538a04e1f481bb0c00141c16c159970'}
        response = requests.get(base_url, headers=headers, cookies=cookies, params=query_params)
        if verbose:
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text[:500]}')
        output = response.json()
        try:
            if output['resource_response']['data']:
                output['available'] = False
                output['taken'] = True
            elif not output['resource_response']['data']:
                output['available'] = True
                output['taken'] = False
        except Exception:
            if verbose:
                print(f'Error: {output}')
            return False
    except Exception as e:
        if verbose:
            print(f'Error: {e}')
        return False