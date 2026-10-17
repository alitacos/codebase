def count_occurences_of_substring_in_text(substring:str='', text:str='')->int:
    if text and substring:
        return text.count(substring)