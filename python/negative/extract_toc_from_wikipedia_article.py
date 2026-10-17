#extract_headings_from_wikipedia_url_2
 # even if no error, the code would not get the expected results. Code has no structure, no functions, no exceptions, no strategy, no reasoned logic ....
import requests
from bs4 import BeautifulSoup

# Example URL of a Wikipedia article
url = 'https://en.wikipedia.org/wiki/Wikipedia:Directories_and_indexes#Content_administration'

# Send GET request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the main content of the page (usually in <main> tag or an equivalent div)
main_content = soup.find('main', {'id': 'content'})  # For Wikipedia it's usually in <main> tag with id 'content'

# Find the Table of Contents (ToC) within the main content
toc_div = main_content.find('div', id='vector-toc')

# Function to extract headings with order, level, heading text, and href from the ToC
# Function to extract headings with order, level, heading text, and href from the ToC
def extract_toc(toc_div, url):
    toc = []
    
    if toc_div:
        # Recursive function to handle nested ToC items
        def extract_sublist(toc_list, level=1):
            # Find all <li> elements in the ToC, without descending into nested sublists yet
            items = toc_list.find_all('li', recursive=False)
            for idx, item in enumerate(items):
                # Extract <a> tag and get the heading text and href
                link = item.find('a')
                if link:
                    heading_text = link.get_text(strip=True)
                    href = link.get('href')
                    
                    # Handle relative URLs
                    if href and href.startswith('#'):
                        href = urljoin(url, href)
                    
                    order = len(toc) + 1
                    toc.append({
                        'order': order,
                        'level': level,
                        'heading': heading_text,
                        'href': href
                    })
                
                # Check for sublist and process recursively if found
                sublist = item.find('ul')
                if sublist:
                    extract_sublist(sublist, level + 1)

        # Start extracting from the top-level ToC list
        extract_sublist(toc_div, level=1)
    
    return toc
# Extract Table of Contents (ToC)
toc_data = extract_toc(toc_div,url)
