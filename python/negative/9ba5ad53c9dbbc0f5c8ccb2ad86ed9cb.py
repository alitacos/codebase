import collections
from bs4 import BeautifulSoup, Comment
from bs4.element import Tag, NavigableString
import html2text
import re

def split_wonderhowto_article_soup_to_sections(el_name: str , article_tag: Tag ) -> list:
    """
    Split a BeautifulSoup-parsed article into structured sections based on heading tags.
    
    This function iterates through the direct children of an HTML article tag and segments
    the content into logical sections whenever a specified heading element (e.g., h1–h6)
    is encountered. Each section includes the heading, associated body content, extracted
    text, markdown conversion, embedded code blocks, and detected media elements.
    
    The function also preserves pre-heading (introductory) content by treating text nodes
    before the first heading as part of the initial section.
    
    Code blocks inside <pre><code> tags are extracted, converted into fenced markdown,
    and temporarily replaced with placeholders during text conversion to preserve formatting.
    
    Args:
        el_name (str):
            The HTML heading tag name used to split sections (e.g., 'h2').
            Must be one of: 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'.
            If empty or invalid, a ValueError is raised.
    
        article_tag (Tag):
            A BeautifulSoup Tag object representing the root article element to parse.
            Must not be None or a string.
    
    Returns:
        list:
            A list of dictionaries, each representing a section of the article with keys:
                - h2: Raw HTML of the heading element (if present)
                - heading: Plain text heading title
                - section_el: Raw HTML content of the section body
                - text: Cleaned plain text content of the section
                - markdown: Markdown representation of the section including code blocks
                - section: Combined HTML section wrapper
                - code_blocks: List of extracted fenced code blocks
                - media: List of image/figure elements found in the section
                - blocktypes: Sorted list of detected element types (code, media, headings)
                - sub_sections: List of nested heading tags within the section
    
    Example usage:
        >>> result = split_wonderhowto_article_soup_to_sections(el_name='h2', article_tag=BeautifulSoup(html,'html.parser').find('div',{'id':'contents'}))
    """
    sections = []
    current_section_elements_html = ''
    current_section_title_html = None

    def create_section_dict(h2_html, body_html):
        h2_str = h2_html if h2_html else ""
        soup_h2 = BeautifulSoup(h2_str, 'html.parser')
        heading_md = soup_h2.get_text(strip=True)

        temp_soup = BeautifulSoup(body_html, 'html.parser')
        clean_text = temp_soup.get_text(separator=' ', strip=True)

        # ✅ FIX #1: do NOT drop valid pretext accidentally
        # only drop truly empty garbage
        if not heading_md and not clean_text:
            return None

        code_blocks = []
        code_types = []
        placeholder_map = {}
        placeholder_idx = 0

        for pre_tag in temp_soup.find_all('pre'):
            code_tag = pre_tag.find('code')
            content = code_tag.get_text() if code_tag else pre_tag.get_text()

            lang = "raw"
            classes = (pre_tag.get('class', []) + (code_tag.get('class', []) if code_tag else []))

            for cls in classes:
                if isinstance(cls, str):
                    if 'lang-' in cls or 'language-' in cls:
                        lang = cls.split('-')[-1]
                        break
                    elif cls.lower() in ['python', 'bash', 'js', 'javascript', 'html', 'css']:
                        lang = cls.lower()
                        break

            fenced = f"\n```{"raw" if lang == '' else lang}\n{content.strip()}\n```\n"
            code_blocks.append(fenced)
            code_types.append(lang)

            # Replace the pre_tag with a unique placeholder
            placeholder = f"_CODE_BLOCK_PLACEHOLDER_{placeholder_idx}_"
            placeholder_map[placeholder] = fenced
            pre_tag.replace_with(NavigableString(placeholder))
            placeholder_idx += 1

        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0

        header_markdown = h.handle(h2_str).strip()
        body_raw_md = h.handle(str(temp_soup)) # Now temp_soup has placeholders

        # Replace placeholders in the markdown
        for placeholder, fenced_code in placeholder_map.items():
            body_raw_md = body_raw_md.replace(placeholder, fenced_code)

        full_markdown = (header_markdown + "\n\n" + body_raw_md).strip()
        figures= [i  for i in temp_soup.find_all(['img','figure']) if i and  "cnx-pod-loading-background" not in i.get('class','')   ]
        return {
            'h2': h2_str,
            'heading': heading_md,
            'section_el': body_html,
            'text': clean_text,
            'markdown': full_markdown,
            'section': f'<section>{h2_str}{body_html}</section>',
            'code_blocks': code_blocks,
            'media':figures,

            "blocktypes": sorted(set((code_types if code_types else []) +    ( [i.name for i in figures if i]) + ( [i.name for i in temp_soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]) if i]))) ,
            'sub_sections': [str(i).strip() for i in temp_soup.find_all(['h1','h2','h3','h4','h5','h6'])],
        }
        h2 = current_heading.get_text(strip=True) if current_heading else None
        
 
 
    for element in article_tag.children:
        if isinstance(element, Comment):
            continue

        if isinstance(element, Tag) and element.name in ['script', 'meta', 'style', 'link']:
            continue

        # keep your logic, but FIX text handling
        if isinstance(element, NavigableString):
            txt = str(element).strip()

            # ❌ FIX #2: don't blindly skip everything
            if not txt or txt.startswith('#//'):
                continue

            # pretext MUST be preserved
            current_section_elements_html += txt + " "
            continue

        if isinstance(element, Tag) and element.name == el_name:
            if current_section_title_html or current_section_elements_html.strip():
                sec_dict = create_section_dict(
                    current_section_title_html,
                    current_section_elements_html
                )
                if sec_dict:
                    sections.append(sec_dict)

            current_section_title_html = str(element)
            current_section_elements_html = ''
        else:
            current_section_elements_html += str(element)

    # final flush (important for pretext-only pages)
    if current_section_title_html or current_section_elements_html.strip():
        sec_dict = create_section_dict(
            current_section_title_html,
            current_section_elements_html
        )
        if sec_dict:
            sections.append(sec_dict)

    return sections
