def check_if_can_get_local_json_keys_via_json_load(obj:str=None, filepath) -> bool:
    #somehow it makes not much sense. readability is not good. 
    """
    Retrieve first layer and nested keys from a local JSON file.
    
    This function reads a JSON file from the given file path, extracts the keys
    from the top layer, and then extracts nested keys from the JSON structure.
    
    Args:
    - file_path (str): The path to the JSON file.
    
    Returns:
    - tuple: A tuple containing two lists: first_layer_keys and nested_keys.
             first_layer_keys (list): Keys from the top layer of the JSON.
             nested_keys (list): Keys from the nested JSON structure.
    """
    import json
    
    if not filepath and obj:         
        try:
            # Open and read the JSON file
            #with open(file_path, 'r') as f:
            data = json.load(obj)  # Load JSON data from the file
            # Extract keys from the top layer
            first_layer_keys = list(data.keys())
            # Extract nested keys from the JSON structure
            nested_keys = get_nested_keys(data)
            return 1
        except Exception as e:
            return  0
    elif filepath and not obj:
        try:
            # Open and read the JSON file
            with open(file_path, 'r') as f:
                data = json.load(obj)  # Load JSON data from the file
                # Extract keys from the top layer
                first_layer_keys = list(data.keys())
                # Extract nested keys from the JSON structure
                nested_keys = get_nested_keys(data)
                return 1
        except Exception as e:
            return  0

    elif not obj and not filepath:
        return 0
    else:
        results = []
        try:
            # Open and read the JSON file
            #with open(file_path, 'r') as f:
            data = json.load(obj)  # Load JSON data from the file
            # Extract keys from the top layer
            first_layer_keys = list(data.keys())
            # Extract nested keys from the JSON structure
            nested_keys = get_nested_keys(data)
            check1 = 1
        except Exception as e:
            check1 = 0
        try:
            # Open and read the JSON file
            with open(file_path, 'r') as f:
                data = json.load(obj)  # Load JSON data from the file
                # Extract keys from the top layer
                first_layer_keys = list(data.keys())
                # Extract nested keys from the JSON structure
                nested_keys = get_nested_keys(data)
                check2 = 1
        except Exception as e:
            check2 = 0
        return (check1+check2)/2
