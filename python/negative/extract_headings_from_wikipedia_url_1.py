# code has SyntaxError. even if no syntax error, the code would not get the expected results. Code has no structure, no functions, no exceptions, no strategy, no reasoned logic ....
#  Cell In[2], line 28,    obj = {'section':{'id': idx, 'level': int(i.name[-1]), 'heading':{'content':{'text':i.get_text(strip=True)}}, 'contents':list, 'subheaders':list,'raw':str.splitlines(), 'markdown':str.splitlines()}  ^  SyntaxError: '{' was never closed

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/wiki/Lists_of_sovereign_states_and_dependent_territories#Miscellaneous'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

footer_cards = soup.find_all('div', {'class': 'navbox'})
df = pd.read_html(str(footer_cards[0]))[0]
print(len(df))
print(df.head())
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = 'https://en.wikipedia.org/wiki/Lists_of_sovereign_states_and_dependent_territories#Miscellaneous'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

idx = 0
headings = []  # ✅ Initialize the list before using it

# Extract all heading tags (h1 to h6)
for i in soup.find_all(re.compile('^h[1-6]$')):
    #x : list = None # we add x as sub sections contents items  'contents':[i for i in x]}. if raw or plain_md we add a single section into raw
    obj = {'section':{'id': idx, 'level': int(i.name[-1]), 'heading':{'content':{'text':i.get_text(strip=True)}}, 'contents':list, 'subheaders':list,'raw':str.splitlines(), 'markdown':str.splitlines()}
    idx += 1
    headings.append(obj)

# Print the headings to verify
for h in headings:
    print(h)