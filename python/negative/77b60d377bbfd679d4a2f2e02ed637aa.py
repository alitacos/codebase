def store_html(url:str='', html:str='',  target_dir:str='',file_name:str='', index_source:str='',tmp_source:str='' ,extensions:list=[])->bool:
    """
        Stores HTML content to a local filesystem path and updates processing logs accordingly.

        The function:
        - Creates the target directory if it does not exist
        - Writes HTML content into a file
        - Appends the processed URL to an index log file
        - Removes the URL from a temporary processing log file

    Args:
        url (str): Source URL associated with the HTML content. (Defaults to '')
        html (str): Raw HTML content to be written to disk. (Defaults to '')
        target_dir (str): Directory where the HTML file will be stored. (Defaults to '')
        file_name (str): Name of the HTML file to be created. (Defaults to '')
        index_source (str): Path to the index file tracking successfully processed URLs. (Defaults to '')
        tmp_source (str): Path to the temporary file tracking pending URLs. (Defaults to '')
        extensions (list): Allowed file extensions used for validating index file writes. (Defaults to [])

    Returns:
        bool: True if HTML was successfully written and logs were updated, False otherwise.

    Example usage:
        >>> result = store_html(url='[MASKED]', html='[MASKED]', target_dir='[MASKED]', file_name='[MASKED]', index_source='[MASKED]', tmp_source='[MASKED]', extensions='[MASKED]')
    """
    import os
    try:
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, file_name), 'w') as f:
            f.write(html)
        append_line_as_url_in_txt_file(path=index_source, url=url, extensions=extensions)
        remove_url_line_from_txt_file(path=tmp_source, url=url)
        return True
    except Exception as e:
        #print(f"Error writing HTML for {url}: {e}")
        return False