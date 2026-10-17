#test
def extract_table_of_contents_from_arxiv_article_html(html: str = None) -> dict:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html or "", "html.parser")
    article = soup.find("article")

    if article is None:
        return {
            "title": None,
            "title_element": None,
            "chapter_heading": None,
            "sub_heading": None,
            "headings": [],
            "heading_counts": {},
            "pretext": None,
            "chapters": [],
        }

    heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]

    # ------------------------------------------------------------
    # 1. Find title + all headings
    # ------------------------------------------------------------

    html_title = soup.find("title")

    headings = article.find_all(heading_tags)

    heading_counts = {
        level: len(article.find_all(level))
        for level in heading_tags
    }

    used_levels = [
        int(level[1:])
        for level in heading_tags
        if heading_counts[level] > 0
    ]

    lowest_level = min(used_levels) if used_levels else None

    # First meaningful article element.
    article_elements = [
        e for e in article.children
        if getattr(e, "name", None)
    ]

    first_heading = next(
        (e for e in article_elements if e.name in heading_tags),
        None
    )

    first_heading_is_at_top = (
        first_heading is not None
        and article_elements
        and article_elements[0] is first_heading
    )

    # ------------------------------------------------------------
    # 2. Infer title / chapter / subsection hierarchy
    # ------------------------------------------------------------

    title = None
    title_element = None
    chapter_level = None
    subsection_level = None

    # ------------------------------------------------------------
    # CASE A
    #
    # Lowest = h1
    #
    # One h1 at the top:
    #
    #     h1 = article title
    #     h2 = chapter
    #     h3+ = subsection
    #
    # ------------------------------------------------------------

    if (
        lowest_level == 1
        and heading_counts["h1"] == 1
        and first_heading_is_at_top
    ):
        title_element = first_heading
        title = first_heading.get_text(" ", strip=True)

        # First higher heading becomes chapter splitter.
        higher_levels = [
            level for level in used_levels
            if level > 1
        ]

        if higher_levels:
            chapter_level = min(higher_levels)

            even_higher = [
                level for level in higher_levels
                if level > chapter_level
            ]

            if even_higher:
                subsection_level = min(even_higher)

    # ------------------------------------------------------------
    # CASE B
    #
    # Lowest = h1
    # More than one h1:
    #
    #     h1 = chapter
    #     h2+ = subsection
    #
    # ------------------------------------------------------------

    elif (
        lowest_level == 1
        and heading_counts["h1"] > 1
    ):
        chapter_level = 1

        higher_levels = [
            level for level in used_levels
            if level > 1
        ]

        if higher_levels:
            subsection_level = min(higher_levels)

    # ------------------------------------------------------------
    # CASE C
    #
    # No h1.
    # Exactly one h2 at top:
    #
    #     h2 = article title
    #     h3 = chapter
    #     h4+ = subsection
    #
    # ------------------------------------------------------------

    elif (
        lowest_level == 2
        and heading_counts["h2"] == 1
        and first_heading_is_at_top
    ):
        title_element = first_heading
        title = first_heading.get_text(" ", strip=True)

        higher_levels = [
            level for level in used_levels
            if level > 2
        ]

        if higher_levels:
            chapter_level = min(higher_levels)

            even_higher = [
                level for level in higher_levels
                if level > chapter_level
            ]

            if even_higher:
                subsection_level = min(even_higher)

    # ------------------------------------------------------------
    # CASE D
    #
    # No title-like heading:
    #
    # Multiple h2:
    #     h2 = chapter
    #
    # Multiple h1:
    #     h1 = chapter
    #
    # The lowest heading is therefore the chapter splitter.
    # ------------------------------------------------------------

    elif lowest_level is not None:
        chapter_level = lowest_level

        higher_levels = [
            level for level in used_levels
            if level > chapter_level
        ]

        if higher_levels:
            subsection_level = min(higher_levels)

    # ------------------------------------------------------------
    # No headings at all
    # ------------------------------------------------------------

    if lowest_level is None:
        pretext = BeautifulSoup(
            "".join(str(e) for e in article_elements),
            "html.parser"
        )

        return {
            "title": html_title,
            "title_element": None,
            "chapter_level": None,
            "subsection_level": None,
            "headings": [],
            "heading_counts": heading_counts,
            "pretext": pretext,
            "chapters": [],
        }

    # ------------------------------------------------------------
    # 3. Remove article title from the stream.
    #
    # We don't want the article title to become pretext/chapter.
    # ------------------------------------------------------------

    if title_element is not None:
        title_element = title_element

    # ------------------------------------------------------------
    # 4. Flatten article into heading-aware elements.
    #
    # Sections are transparent.
    #
    # If a DIV contains headings, recursively split it.
    # ------------------------------------------------------------

    def contains_heading(element):
        return element.find(heading_tags) is not None

    def flatten(element):
        """
        Convert arbitrary nested article HTML into a flat sequence
        where headings are always individual elements.
        """

        if not getattr(element, "name", None):
            return

        if element.name in heading_tags:
            yield element
            return

        # Don't keep section wrappers.
        if element.name == "section":
            for child in element.children:
                if getattr(child, "name", None):
                    yield from flatten(child)
            return

        # Element contains headings -> recursively expose them.
        if contains_heading(element):
            for child in element.children:
                if getattr(child, "name", None):
                    yield from flatten(child)
            return

        # Ordinary content stays intact.
        yield element

    flat_elements = []

    for element in article_elements:
        # Don't emit article title as content.
        if title_element is not None and element is title_element:
            continue

        flat_elements.extend(flatten(element))

    # ------------------------------------------------------------
    # 5. Split article into chapters.
    #
    # Before first chapter heading = pretext.
    #
    # Every heading at chapter_level starts a chapter.
    # Higher headings remain inside that chapter and are handled
    # in the subsection/block phase.
    # ------------------------------------------------------------

    pretext_elements = []
    chapters_raw = []

    current_chapter = None

    for element in flat_elements:

        if (
            element.name in heading_tags
            and int(element.name[1:]) == chapter_level
        ):
            if current_chapter is not None:
                chapters_raw.append(current_chapter)

            current_chapter = [element]

        else:
            if current_chapter is None:
                pretext_elements.append(element)
            else:
                current_chapter.append(element)

    if current_chapter is not None:
        chapters_raw.append(current_chapter)

    # ------------------------------------------------------------
    # 6. Build pretext
    # ------------------------------------------------------------

    pretext = None

    if pretext_elements:
        pretext_soup = BeautifulSoup(
            "".join(str(e) for e in pretext_elements),
            "html.parser"
        )

        if pretext_soup.get_text(strip=True):
            pretext = pretext_soup

    # ------------------------------------------------------------
    # 7. Split each chapter into blocks.
    #
    # A block starts at:
    #
    #     chapter heading
    #     subsection heading
    #
    # and continues until the next relevant heading.
    #
    # Importantly, nested elements containing headings have already
    # been flattened above.
    # ------------------------------------------------------------

    def split_chapter(chapter_elements):
        blocks = []
        current_block = []

        for element in chapter_elements:

            is_heading = element.name in heading_tags

            if is_heading:
                level = int(element.name[1:])

                # Chapter heading itself starts the first block.
                if level == chapter_level:
                    if current_block:
                        blocks.append(
                            BeautifulSoup(
                                "".join(current_block),
                                "html.parser"
                            )
                        )

                    current_block = [element]

                # Any higher-level heading starts a subsection block.
                elif (
                    subsection_level is not None
                    and level >= subsection_level
                ):
                    if current_block:
                        blocks.append(
                            BeautifulSoup(
                                "".join(current_block),
                                "html.parser"
                            )
                        )

                    current_block = [element]

                else:
                    current_block.append(element)

            else:
                current_block.append(element)

        if current_block:
            blocks.append(
                BeautifulSoup(
                    "".join(current_block),
                    "html.parser"
                )
            )

        return blocks

    chapters = [
        split_chapter(chapter)
        for chapter in chapters_raw
    ]

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