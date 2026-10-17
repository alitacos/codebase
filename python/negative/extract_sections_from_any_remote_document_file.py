from bs4 import BeautifulSoup

# Replace this with your actual HTML content
# soup = BeautifulSoup(html_content, 'html.parser')

main = soup.find('main')
if not main:
    print("❌ <main> not found.")
    exit()

# Collect all elements after the first .relative.group heading
sections = []
current_section = {'heading': None, 'text': ''}
collecting = False

# Loop through all elements in the main
for el in main.descendants:
    if isinstance(el, str):  # Skip direct strings (text nodes)
        continue
    
    # Skip unwanted tags like script, style, nav, etc.
    if el.name in ['script', 'style', 'nav', 'a', 'iframe', 'main', 'body']:
        continue
    
    # Check if it's a heading with class="relative group"
    if el.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and 'relative' in el.get('class', []) and 'group' in el.get('class', []):
        # If we already have a section collected, save it
        if current_section['text'].strip():
            sections.append(current_section)
        
        # Start a new section with this heading
        heading_text = el.get_text(strip=True)
        current_section = {'heading': heading_text, 'text': ''}
        collecting = True  # Start collecting text for this section
    else:
        # Collect text for the current section (if we're in a section)
        if collecting:
            text = el.get_text(strip=True)  # Keep formatting
            if text:
                current_section['text'] += text + '\n'

# Add the last collected section if there's any text
if current_section['text'].strip():
    sections.append(current_section)

# If no headings were found and text exists, wrap it in a section with heading=None
if not sections and current_section['text'].strip():
    sections.append(current_section)

# Output the sections in the required format
for i, sec in enumerate(sections, 1):
    print(f"--- Section {i} ---")
    print(f"Heading: {sec['heading']}")
    print(f"Text:\n{sec['text'].strip()}\n")
#print(sections[0]['text']#out:IndexError
 