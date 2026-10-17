import re
#NEGATIVE
#The function works if a docstring has some spesific form but is not correctly identifing blocks if have no colon
def  parse_docstring_via_re_into_blocks(docstring: str) -> dict:
    """
    Parses a Google-style Python docstring into structured components using regex-based heuristics.

    The parser attempts to extract:
    - A one-line summary
    - A longer free-form description
    - Arguments (Args / Parameters section)
    - Return value specification
    - Raised exceptions

    It supports common Google-style docstring variations and performs light normalization
    of whitespace and multi-line sections. Parsing is heuristic-based and may not cover
    all edge cases of complex or non-standard docstrings.

    Args:
        docstring (str): The docstring string to parse. Should follow Google-style
            formatting conventions for best results.

    Returns:
        dict: A structured dictionary with the following keys:
            - "summary" (str): First line of the docstring
            - "description" (str): Extended description body
            - "args" (list): List of parsed argument dictionaries
            - "returns" (dict): Parsed return type and description
            - "raises" (list): List of raised exception dictionaries

    Example usage:
        >>> result = parse_docstring_via_re_into_blocks(docstring=\"\"\"[MASKED]\"\"\")
        >>> print(result["args"])
    """
    parsed_data = {
        "summary": "",
        "description": "",
        "args": [],
        "returns": {},
        "raises": []
    }

    if not docstring:
        return parsed_data

    # Normalize newlines and strip overall whitespace
    clean_docstring = docstring.strip().replace('\r\n', '\n').replace('\r', '\n')
    lines = clean_docstring.split('\n')

    # Extract summary (first non-empty line)
    if lines:
        parsed_data["summary"] = lines[0].strip()
        lines = lines[1:] # Remaining lines

    current_section = "description"
    description_lines = []
    current_arg = None # For multi-line arg descriptions
    current_raise = None # For multi-line raise descriptions

    section_map = {
        "Args:": "args",
        "Arguments:": "args",
        "Parameters:": "args",
        "Returns:": "returns",
        "Return:": "returns",
        "Raises:": "raises",
        "Raise:": "raises",
    }

    # Iterate through lines to parse sections
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            # Empty line, reset current_arg/current_raise if not in a specific section
            if current_section == "args" and current_arg:
                current_arg = None
            if current_section == "raises" and current_raise:
                current_raise = None
            continue

        # Check for new section headers
        is_section_header = False
        for header, section_name in section_map.items():
            if stripped_line.startswith(header):
                current_section = section_name
                is_section_header = True
                break
        
        if is_section_header:
            continue

        # Process lines based on the current section
        if current_section == "description":
            description_lines.append(stripped_line)
        elif current_section == "args":
            # Example: param (type, optional): Description
            # Example: param (type): Description
            arg_match = re.match(r'^(?P<name>\w+)\s*\((?P<type>[^)]+)\):(?P<description>.*)$', stripped_line)
            if arg_match:
                arg_data = arg_match.groupdict()
                arg_type_part = arg_data['type'].strip()
                
                arg_type = arg_type_part
                is_optional = False
                default_val = None

                # Check for optional and default
                if ', optional' in arg_type_part.lower():
                    is_optional = True
                    arg_type = arg_type_part.replace(', optional', '').replace(',Optional', '').strip()
                
                # Simplified default extraction (might need more robust regex for complex defaults)
                default_match = re.search(r'Defaults to (?P<default_val>.*)\.', arg_data['description'])
                if default_match:
                    default_val = default_match.group('default_val').strip()
                    # Remove default info from description
                    arg_data['description'] = arg_data['description'].replace(default_match.group(0), '').strip()


                current_arg = {
                    "name": arg_data["name"],
                    "type": arg_type,
                    "optional": is_optional,
                    "default": default_val,
                    "description": arg_data["description"].strip()
                }
                parsed_data["args"].append(current_arg)
            elif current_arg:
                # Continuation of previous argument's description
                current_arg["description"] += " " + stripped_line
        elif current_section == "returns":
            # Example: type: Description of return value.
            return_match = re.match(r'^(?P<type>[^:]+):\s*(?P<description>.*)$', stripped_line)
            if return_match:
                parsed_data["returns"] = return_match.groupdict()
                parsed_data["returns"]["type"] = parsed_data["returns"]["type"].strip()
                parsed_data["returns"]["description"] = parsed_data["returns"]["description"].strip()
            elif parsed_data["returns"]:
                 parsed_data["returns"]["description"] += " " + stripped_line
        elif current_section == "raises":
            # Example: Exception: Description of when this exception is raised.
            raise_match = re.match(r'^(?P<type>[^:]+):\s*(?P<description>.*)$', stripped_line)
            if raise_match:
                current_raise = raise_match.groupdict()
                current_raise["type"] = current_raise["type"].strip()
                current_raise["description"] = current_raise["description"].strip()
                parsed_data["raises"].append(current_raise)
            elif current_raise:
                current_raise["description"] += " " + stripped_line

    parsed_data["description"] = "\n".join(description_lines).strip()

    # If description is empty and summary is present, move summary to description if multi-line summary was unintended
    if not parsed_data["description"] and '\n' in parsed_data["summary"]:
        summary_lines = parsed_data["summary"].split('\n')
        parsed_data["summary"] = summary_lines[0].strip()
        parsed_data["description"] = '\n'.join(summary_lines[1:]).strip()

    return parsed_data
