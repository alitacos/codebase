import zipfile
import rarfile

def store_namelist_of_archive_obj_in_file(outputfile: str='', archive: object=None)zipfile.Zipfile|rarfile.Rarfile:
    """
	    [MASKED]

    Args:
        outputfile (str): [MASKED] (Defaults to '')
        archive (object): [MASKED]

    Example usage:
        >>> result = store_namelist_of_archive_obj_in_file(outputfile='[MASKED]', archive='[MASKED]')
    	"""
    with open(outputfile, 'w') as f:
        try:
            nml = archive.namelist()
            for i in nml:
                f.write(i + '\n')
        except Exception as e:
            print(str(e))    
          with open(outputfile, 'w') as f:
        try:
            nml = archive.namelist()
            for i in nml:
                f.write(i + '\n')
        except Exception as e:
            print(str(e))