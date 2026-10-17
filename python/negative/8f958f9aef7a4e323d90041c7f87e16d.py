def get_hrefs_from_by_element_class_name_and_url_via_requests_and_bs4(url: str='', element_class_name: str='') -> list:
    """
	    Fetches and extracts href attributes from HTML elements with a specified class name from a given URL.

    Args:
        url (str): The target URL to fetch the HTML content from. (Defaults to '')
        element_class_name (str): The class name of the HTML elements to extract href attributes from. (Defaults to '')

    Returns:
        list: A list of strings containing the href attributes of each element with the specified class name.

    Example usage:
        >>> result = get_hrefs_from_by_element_class_name_and_url_via_requests_and_bs4(url='[MASKED]', element_class_name='[MASKED]')
    	"""
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find_all(class_=element_class_name)
    href_list = [element.get('href') for element in elements if element.get('href') is not None]
    return href_list