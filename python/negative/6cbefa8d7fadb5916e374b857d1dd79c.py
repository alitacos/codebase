def collect_csv_code_sources_from_local_path_via_glob(path: str='') -> list:
    import glob
    if not path:
        return []
      
    if path.endswith('.csv'):
        return glob.glob(path, recursive=True)
    return glob.glob(f"{path.rstrip('/')}/**/*.csv", recursive=True)