# code has SyntaxError. even if no syntax error, the code would not get the expected results. Code has no structure, no functions, no exceptions, no strategy, no reasoned logic ....
import requests

# Define the API endpoint
url = "https://en.wikipedia.org/w/api.php"

# Get section information
params = {
    'action': 'parse',
    'format': 'json',
    'page': 'Outline_of_Hinduism',
    'prop': 'sections',
    'formatversion': 2
}

response = requests.get(url, params=params)
data = response.json()
print(data['parse'].keys())

sections = data['parse']['sections']

# Fetch content for each section
section_details = []

for section in sections:
    section_id = section['index']
    section_title = section['line']
    section_url = f"https://en.wikipedia.org/wiki/Outline_of_Hinduism#{section['anchor']}"

    # Fetch the section content in plain text
    section_params = {
        'action': 'query',
        'format': 'json',
        'titles': 'Outline_of_Hinduism',
        'prop': 'extracts',
        'explaintext': True,
        'section': section_id
    }
    
    section_response = requests.get(url, params=section_params)
    section_data = section_response.json()

    page_id = next(iter(section_data['query']['pages']))
    section_content = section_data['query']['pages'][page_id].get('extract', 'No content available.')
    print()
    section_details.append({
        'id': section_id,
        'heading': section_title,
        'source': section_url,
        'content': section_content
    })

# Final object with sections
output = {
    'source': 'https://en.wikipedia.org/wiki/Outline_of_Hinduism',
    'title': 'Outline of Hinduism',
    'type': 'document',
    'toc': [{'section_number': i['index'], 'heading_text': i['line'], 'href': f"https://en.wikipedia.org/wiki/Outline_of_Hinduism#{i['anchor']}"} for i in sections],
    'content': {'sections': section_details}
}

# Print the result
import json
print(json.dumps(output, indent=2))
