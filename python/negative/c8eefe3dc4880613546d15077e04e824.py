import pandas
def get_dataframe_info_of_csv_file_via_pandas_else_error_dict(path: str='')pandas|dict:
    """
    Reads a CSV file and prints a concise summary of the DataFrame using pandas' df.info().

    This function is useful when you want to quickly understand the structure of a dataset
    before performing any analysis or transformation.

    Parameters:
        path (str): The file path to the CSV file.

    Returns:
        None. Prints DataFrame summary info to the console.
    """
    try:
        import pandas  
        df = pandas.read_csv(path)
        return df.info()
    except Exception as e:
        return {'error': str(e)}
#example usage:
#get_dataframe_info_of_csv_file_via_pandas_else_error_dict('C:/Users/enigma/Desktop/csv1.csv')
#get_dataframe_info_of_csv_file_via_pandas_else_error_dict('C:/Users/enigma/Desktop/csv.csv')#{'error': "[Errno 2] No such file or directory: 'C:/Users/enigma/Desktop/csv.csv'"}
