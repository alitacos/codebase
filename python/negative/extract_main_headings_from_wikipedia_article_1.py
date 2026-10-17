
# Function to extract main content headings
def extract_main_headings(main_content):
    headings = []
    # Find all headings (h1, h2, h3, etc.) in the main content
    all_headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    for idx, heading in enumerate(all_headings):
        heading_text = heading.get_text(strip=True)
        href = heading.find('a').get('href') if heading.find('a') else None  # Get link if available
        level = int(heading.name[1])  # Level from the tag name, i.e., h2 is level 2, h3 is level 3, etc.
        headings.append({'order': idx + 1, 'level': level, 'heading': heading_text, 'href': href})
    
    return headings

# Extract main content headings
main_headings = extract_main_headings(main_content)

# Print the extracted Table of Contents (ToC) and Main Content headings
#print("Table of Contents:")
#for entry in toc_data:
#    print(f"Order: {entry['order']}, Level: {entry['level']}, Heading: {entry['heading']}, Href: {entry['href']}")

#print("\nMain Content Headings:")
#for entry in main_headings:
#    print(f"Order: {entry['order']}, Level: {entry['level']}, Heading: {entry['heading']}, Href: {entry['href']}")
toc_data