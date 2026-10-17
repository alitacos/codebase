def get_github_root_directory_tree_via_github_api_and_requests(owner: str='', repo: str='', branch: str='', token: str='') -> list:
    import requests
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/'
    headers = {'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    params = {}
    if branch:
        params['ref'] = branch
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return None