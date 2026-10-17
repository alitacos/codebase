def extract_zipfile_to_output_directory_and_print_status(file_path = None,output_dir =None):
    """ # THIS CODE (commented in docstring) IS NOT WORKING WELL. PREFERE CODE LIKE:
    def extract_zipfile_to_output_directory_and_print_status(file_path = None,output_dir =None):
        import zipfile
        import os
        from pprint import pprint
        # Inputs
        file_path = "files.zip"
        
        # Outputs
        output_dir = "zip_extraction"
        # Create output dir
        os.mkdir(output_dir)
        
        # Extract files
        if os.path.exists(file_path):
            # open the zip file for reading
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # extract all files to the current working directory
                zip_ref.extractall(output_dir)
        else:
            print(f"❌ ZIP path '{file_path}' does not exist. Please update it on your variables.")
            print("Number of files extracted:", len(os.listdir(output_dir)))
        pprint(os.listdir(output_dir))
    """
    import zipfile
    import os
    from pprint import pprint
    if output_dir:
        output = output_dir
    else:
        output = '.'.join(file_path.split('.')[:-1]).strip('.')
        

    # Extract files
    if os.path.exists(file_path):
        try:
            # open the zip file for reading
            with zipfile.ZipFile(file_path, 'r') as rar_ref:
                # extract all files to the current working directory
                # Create output dir
                os.mkdir(output)
                rar_ref.extractall(output)
                print("Number of files extracted:", len(os.listdir(output)))
                pprint(os.listdir(output))
        except Exception as e:
            print(f"❌ ERROR '{file_path}' : {str(e)}")
    else:
        print(f"❌ ERROR '{file_path}' does not exist. Please update it on your variables.")
        
# Example usage  
# extract_rarfile_to_output_directory_and_print_status(file_path = "files.rar",output_dir = "rar_extraction")