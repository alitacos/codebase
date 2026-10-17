def change_the_delimiter_of_csv_and_rename_or_store_in_destination(input_path:str='', output_path:str='', delimiter:str='\t', deleteInput:bool=False) -> dict:
    """
    Change the delimiter of a CSV file and optionally overwrite or save to a new file.

    Reads a CSV file using its existing delimiter and writes it with a new delimiter.
    Can overwrite the original file or save to a different destination. Optionally
    deletes the input file after successful processing.

    Args:
        input_path (str): Path to the source CSV file.
        output_path (str): Path to save the modified CSV file. If empty, input file is overwritten.
        delimiter (str): New delimiter to use when writing the CSV.
        deleteInput (bool): If True and output_path differs from input_path, deletes the original file.

    Returns:
        dict: Result information including:
              - input_source: original file path
              - output_source: output file path
              - fieldnames: detected CSV headers
              - delimiter: new delimiter used
              - delimiter_changed: True if operation succeeded
              - error: exception object if failure occurred, otherwise empty dict

    Example usage:
        result = change_the_delimiter_of_csv_and_rename_or_store_in_destination(input_path="input.csv",output_path="output.csv",delimiter=";")
    """
    import csv
    fieldnames = []
    reader = []
    if input_path and not output_path: # we rename the old version
        output_path = input_path
    try:
        with open(input_path, 'r', encoding='utf-8') as infile 
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
        with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            for row in reader:  
                writer.writerow(row)
        if deleteInput and input_path != output_path:
            import os
            os.remove(input_path)
        return {'input_source':input_path, 'output_source': output_path, 'fieldnames':fieldnames,'delimiter':delimiter, 'delimiter_changed':True, 'error':{}}          
    except Exception as e:
        return {'input_source':input_path, 'output_source': output_path, 'fieldnames':fieldnames,'delimiter':delimiter, 'delimiter_changed':True, 'error':e}