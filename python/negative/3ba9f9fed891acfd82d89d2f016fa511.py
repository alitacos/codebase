def get_article_urls_over_infosecwriteups_sitemap(xml_url:str='https://infosecwriteups.com/sitemap/sitemap.xml')->list:
    """
    Fetches and extracts article URLs from the InfoSec Write-ups sitemap.

    This function retrieves the sitemap XML from InfoSec Write-ups, parses it,
    and extracts all URLs listed in <loc> tags. It filters out tag-related URLs
    (i.e., those containing '/tagged/') and returns a deduplicated list of article links.

    Args:
        xml_url (str): URL of the InfoSec Write-ups sitemap XML file 
                       (Defaults to 'https://infosecwriteups.com/sitemap/sitemap.xml')

    Returns:
        list: A sorted list of unique article URLs excluding tag pages

    Example usage:
        >>> result = get_article_urls_over_infosecwriteups_sitemap(xml_url='https://infosecwriteups.com/sitemap/sitemap.xml')
    """
    import requests
    from bs4 import BeautifulSoup
    urls = []
    try:
        response = requests.get(xml_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        sitemap_content = response.content
        soup = BeautifulSoup(sitemap_content, 'xml')
        # Sitemaps can contain <urlset> with <url> tags or <sitemapindex> with <sitemap> tags.
        # Handle both cases recursively if needed, but for a single sitemap.xml with loc tags, this is enough.
        for loc_tag in soup.find_all('loc'):
            url = loc_tag.text
            if "/tagged/" not in url and url not in urls:
                urls.append(url)
        #print(f"Found {len(urls)} URLs without '/tagged/' in the path:")
        return sorted(set(urls))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sitemap: {e}")
        return list()
    except Exception as e:
        print(f"An error occurred: {e}")
        return list()