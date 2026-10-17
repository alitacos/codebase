# method works, but the name ad output do not exactly match the info. Sounds like it should return bool if write action does not work or True if worked...

def write_all_archive_paths_in_path_system_output_file(path: str='', output: str='') -> list:
    """
    Writes the paths of archive files to the given output file and returns the list of archive paths.

    Args:
        tree (list): A list of file paths.
        output (str): The path to the output file.

    Returns:
        list: A list of archive file paths.
    """
    if not path or not output:
        return []
    import glob
    archive_paths = []
    tree = glob.glob(path.rstrip('/') + '/**/*', recursive=True)
    with open(output, 'w') as outf:
        for path in sorted(set(tree)):
            if path.endswith('.rar') or path.endswith('.zip'):
                outf.write(path + '\n')
                archive_paths.append(path)
    return archive_paths