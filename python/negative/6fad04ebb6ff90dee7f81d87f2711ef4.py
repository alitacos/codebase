def get_items_from_local_gz_source(source: str=None, verbose: bool=False) -> list:
    import gzip
    import json
    try:
            with gzip.open(source, 'rb') as f:
                items = json.items(f, 'item')
                return items
        except Exception as e:
            if verbose:
                print(str(e))
            return []
    else:
        if verbose:
            print('<source> argument is missing. Provide a valid string')
        return []