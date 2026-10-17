def extract_table_of_contents_from_any_article_html(html: str = None) -> dict:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html or "", "html.parser")
    article = soup.find("article")

    if article is None:
        return {
            "title": None,
            "title_element": None,
            "chapter_level": None,
            "subsection_level": None,
            "headings": [],
            "heading_counts": {},
            "lowest_level": None,
            "pretext": None,
            "chapters": [],
        }

    heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]

    html_title = soup.find("title")
    headings = article.find_all(heading_tags)

    heading_counts = {level: len(article.find_all(level)) for level in heading_tags}
    used_levels = [int(level[1:]) for level in heading_tags if heading_counts[level] > 0]
    lowest_level = min(used_levels) if used_levels else None

    article_elements = [e for e in article.children if getattr(e, "name", None)]

    first_heading = next((e for e in article_elements if e.name in heading_tags), None)
    first_heading_is_at_top = first_heading is not None and article_elements and article_elements[0] is first_heading

    # ------------------------------------------------------------
    # Infer title / chapter / subsection hierarchy
    # ------------------------------------------------------------

    title = None
    title_element = None
    chapter_level = None
    subsection_level = None

    if lowest_level == 1 and heading_counts["h1"] == 1 and first_heading_is_at_top:
        title_element = first_heading
        title = first_heading.get_text(" ", strip=True)

        higher_levels = [level for level in used_levels if level > 1]

        if higher_levels:
            chapter_level = min(higher_levels)

            even_higher = [level for level in higher_levels if level > chapter_level]
            if even_higher:
                subsection_level = min(even_higher)

    elif lowest_level == 1 and heading_counts["h1"] > 1:
        chapter_level = 1

        higher_levels = [level for level in used_levels if level > 1]

        if higher_levels:
            subsection_level = min(higher_levels)

    elif lowest_level == 2 and heading_counts["h2"] == 1 and first_heading_is_at_top:
        title_element = first_heading
        title = first_heading.get_text(" ", strip=True)

        higher_levels = [level for level in used_levels if level > 2]

        if higher_levels:
            chapter_level = min(higher_levels)

            even_higher = [level for level in higher_levels if level > chapter_level]
            if even_higher:
                subsection_level = min(even_higher)

    elif lowest_level is not None:
        chapter_level = lowest_level

        higher_levels = [level for level in used_levels if level > chapter_level]

        if higher_levels:
            subsection_level = min(higher_levels)

    # ------------------------------------------------------------
    # No headings: entire article is pretext
    # ------------------------------------------------------------

    if lowest_level is None:
        pretext = BeautifulSoup("".join(str(e) for e in article_elements), "html.parser")

        if not pretext.get_text(strip=True):
            pretext = None

        return {
            "title": html_title,
            "title_element": None,
            "chapter_level": None,
            "subsection_level": None,
            "headings": [],
            "heading_counts": heading_counts,
            "lowest_level": None,
            "pretext": pretext,
            "chapters": [],
        }

    # ------------------------------------------------------------
    # Flatten nested article elements.
    #
    # A container containing headings is opened recursively so that
    # the headings become individual elements in the stream.
    # ------------------------------------------------------------

    def contains_heading(element):
        return element.find(heading_tags) is not None

    def flatten(element):
        if not getattr(element, "name", None):
            return

        if element.name in heading_tags:
            yield element
            return

        if element.name == "section" or contains_heading(element):
            for child in element.children:
                if getattr(child, "name", None):
                    yield from flatten(child)
            return

        yield element

    flat_elements = []

    for element in article_elements:
        if title_element is not None and element is title_element:
            continue

        flat_elements.extend(flatten(element))

    # ------------------------------------------------------------
    # Split article into chapters.
    #
    # IMPORTANT:
    # Each chapter is kept as ONE BeautifulSoup object.
    # ------------------------------------------------------------

    pretext_elements = []
    chapters = []
    current_chapter = []

    for element in flat_elements:
        is_heading = element.name in heading_tags
        level = int(element.name[1:]) if is_heading else None

        if is_heading and level == chapter_level:
            if current_chapter:
                chapters.append(BeautifulSoup("".join(str(e) for e in current_chapter), "html.parser"))

            current_chapter = [element]
        else:
            if current_chapter:
                current_chapter.append(element)
            else:
                pretext_elements.append(element)

    if current_chapter:
        chapters.append(BeautifulSoup("".join(str(e) for e in current_chapter), "html.parser"))

    # ------------------------------------------------------------
    # Pretext
    # ------------------------------------------------------------

    pretext = None

    if pretext_elements:
        pretext = BeautifulSoup("".join(str(e) for e in pretext_elements), "html.parser")

        if not pretext.get_text(strip=True):
            pretext = None

    return {
        "title": title if title is not None else html_title,
        "title_element": title_element,
        "chapter_level": chapter_level,
        "subsection_level": subsection_level,
        "headings": headings,
        "heading_counts": heading_counts,
        "lowest_level": lowest_level,
        "pretext": pretext,
        "chapters": chapters,
    }
#negative
#r = requests.get('https://developer.chrome.com/codelabs/candle-bluetooth?hl=en#0')#ok
#chapters = extract_table_of_contents_from_any_article_html(r.text).get('chapters',[])
#chapters[1].find_all(['h1','h2','h3','h4','h5','h6'])#.get_text()
