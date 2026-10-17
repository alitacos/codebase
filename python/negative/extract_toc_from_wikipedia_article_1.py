# code has SyntaxError. even if no syntax error, the code would not get the expected results. Code has no structure, no functions, no exceptions, no strategy, no reasoned logic ....
# Define the API endpoint
url = "https://en.wikipedia.org/w/api.php"

# Set the parameters to get content for a specific section
params = {
    'action': 'parse',
    'format': 'json',
    'page': 'Outline_of_Hinduism',
    'section': 1,                  # Section number (use ID from previous step)
    'formatversion': 2
}

# Send the GET request to the Wikipedia API
response = requests.get(url, params=params)
data = response.json()

# Extract the content of the specific section
section_content = data['parse']['text']['*']  # HTML content of the section

# Print the section content (in HTML format)
print(section_content)