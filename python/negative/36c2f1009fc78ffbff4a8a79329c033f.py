
def get_elements_from_html(html: str=''  , tag: str ='') -> list[bs4.element.Tag]:
    """
    Parse HTML and extract all elements matching a given tag.

    This function uses BeautifulSoup to parse the provided HTML string and
    returns all elements matching the specified tag name.

    Args:
        html (str | None): Raw HTML string to parse. If None or invalid, returns [].
        tag (str | None): Tag name to search for (e.g., 'a', 'div', 'span').

    Returns:
        list: A list of BeautifulSoup Tag objects matching the tag.
              Returns an empty list if nothing is found or input is invalid.
    """
    from bs4 import BeautifulSoup
    if not html or not tag:                      # Validate inputs early
        return []

    try:
        soup = BeautifulSoup(html, 'html.parser')  # Parse HTML safely
        elements = soup.find_all(tag)              # Find all matching tags

        return [el for el in elements if el]      # Filter out any falsy elements (rare)
    except Exception:
        return []                                  # Fail safely with empty list