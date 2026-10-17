# uncomplete code


def extract_title_from_wikipedia_url(soup):
    #soup = get_soup_from_wikipedia_url(url)
    title_tag = soup.find('h1', {'id': 'firstHeading'})
    if title_tag:
        span = title_tag.find('span', class_='mw-page-title-main')
        if span:
            return span.text
        else:
            return title_tag.text
    return ""
url = 'https://en.wikipedia.org/wiki/Outline_of_Hinduism#General_reference'

# Get the original title
original_title = extract_title_from_wikipedia_url(soup)
length1 = len(str(soup.contents))
#print(original_title)
print("Original Title:", original_title)

# Modify the title in the soup
soup_ = edit_title_in_soup(soup, new_title)
print(len(str(soup_.contents)))
print(len(str(original_title)))

# Get the modified title
modified_title = extract_title_from_wikipedia_url(soup_)
#print(modified_title)

print("Modified Title:", modified_title)
print(len(str(modified_title)))

# Check if the title was correctly replaced

print("Valid Process by Title:", valid_process_by_title) #Valid Process by Title: 1

valid_process_by_length = 1 if ( length1 - len(str(soup_.contents))) == (len(original_title) - len(modified_title)) else 0
print("Valid Process by length:",valid_process_by_length) #Valid Process by Title: 0


