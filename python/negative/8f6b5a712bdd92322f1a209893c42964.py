import collections
from bs4 import BeautifulSoup, Comment
from bs4.element import Tag, NavigableString
import html2text
import re
# code is missing to annotate figures, code blocks in markdown
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
    if not el_name:
        raise ValueError("el_name is required")
    if el_name and el_name not in ['h1','h2','h3','h4','h5','h6']:
        raise ValueError("el_name must be a heading")
    if not article_tag  :
        
        raise ValueError("article_tag is required")
    if isinstance(article_tag,str)  :
        raise ValueError("article_tag  must be bs4.element.Tag")


    sections = []

    current_heading = None
    current_html = ""

    # -------------------------
    # helpers
    # -------------------------
    def extract_code_blocks(soup):
        code_blocks = []
        blocktypes = []

        for pre in soup.find_all("pre"):
            code = pre.find("code")
            content = (code.get_text() if code else pre.get_text()).strip()

            lang = "raw"
            classes = (pre.get("class", []) or []) + (code.get("class", []) if code else [])

            for c in classes:
                if isinstance(c, str) and ("lang-" in c or "language-" in c):
                    lang = c.split("-")[-1]
                    break

            code_blocks.append({"lang": lang, "content": content})
            blocktypes.append(f"code:{lang}")

        return code_blocks, blocktypes


    def render_md(html_fragment):
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0
        return h.handle(html_fragment).strip()


    def flush():
        nonlocal current_heading, current_html, sections

        if not current_html.strip() and not current_heading:
            return

        frag = BeautifulSoup(current_html, "html.parser")

        code_blocks, blocktypes = extract_code_blocks(frag)

        # remove code for clean text
        for pre in frag.find_all("pre"):
            pre.decompose()

        text = frag.get_text(" ", strip=True)
        markdown = render_md(str(frag))

        h2 = current_heading.get_text(strip=True) if current_heading else None
        figures=[i.name  for i in frag.find_all('img') if i and  "cnx-pod-loading-background" not in i.get('class','')   ]
        sections.append({
            "h2": h2,
            "heading": h2,
            "html": str(frag),
            "text": text,
            "markdown": markdown,
            "code_blocks": code_blocks,
            'img' : figures,
            "blocktypes": sorted(set((blocktypes if blocktypes else []) +    (figures if figures else []) + ( [i.name for i in frag.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]) if i]))) ,
            "sub_sections": [s for s in frag.find_all(["h1", "h2", "h3", "h4", "h5", "h6"] ) if s]})

        current_heading = None
        current_html = ""


    # -------------------------
    # MAIN LOOP
    # -------------------------
    for el in article_tag.children:

        if isinstance(el, Comment):
            continue

        if isinstance(el, Tag) and el.name in ["script", "style", "meta", "link"]:
            continue

        # heading boundary
        if isinstance(el, Tag) and el.name == el_name:
            flush()
            current_heading = el
            continue

        # pretext or body
        if isinstance(el, (Tag, NavigableString)):
            txt = str(el)

            # remove fake JS comments only
            if isinstance(el, NavigableString):
                stripped = txt.strip()
                if not stripped or stripped.startswith("//"):
                    continue

            current_html += txt

    flush()

    return sections
