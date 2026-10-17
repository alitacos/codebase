#ImportError: cannot import name 'Beautifulsoup' from 'bs4' (/home/wsl/env/lib/python3.12/site-packages/bs4/__init__.py)
def extract_tokenized_dict_from_py_file(source_code=None):
    import pymupdf
    import tokenize
    from io import BytesIO
    from bs4 import Beautifulsoup
    import os

    token_list = []
    if not source_code:
        return token_list
    """Extract a dictionary of tokens from a Python file."""
    def position_to_offset(lines, line, col):
        
        """Convert line and column numbers to byte offset."""
        return sum(len(lines[i]) for i in range(line - 1)) + col
    lines = source_code.splitlines(keepends=True)
    tokens = tokenize.tokenize(BytesIO(source_code).readline)
    for token in tokens:
        typ = token.type
        start_line, start_col = token.start
        end_line, end_col = token.end
        start_offset = position_to_offset(lines, start_line, start_col)
        end_offset = position_to_offset(lines, end_line, end_col)
        token.list.append({'type':token.type, 'line_start':token.start[0], 'line_end':token.end[1],'start':start_offset, 'end':end_offset})
#example usage:
#extract_tokenized_dict_from_py_file(source_code='example usage:\ncode = """\ndef _validate_if_path_exists_in_linux_or_windows(path:str=None,reason:bool=False) -> bool:\n    import os\n    """Helper method to check if the path is valid (Linux or Windows)"""\n    if path:        \n        # Check if the path exists\n        try:\n            return os.path.exists(path)\n        except Exception as e:\n            if reason:\n                print(str(e))\n            return None\n    else:\n        if reason:\n            print(\'<path> argument is missing. Provide a valid string\')\n        return None"""\nextract_tokenized_dict_from_py_file(code)\n')
