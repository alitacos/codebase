def convert_html_string_to_markdown(html: str='') -> str:
    """
    Args:
        html (_type_): _description_

    Returns:
        _type_: _description_
    """
    import pypandoc
    markdown = pypandoc.convert_text(html, 'markdown', format='html', extra_args=['--wrap=none'])
    return markdown