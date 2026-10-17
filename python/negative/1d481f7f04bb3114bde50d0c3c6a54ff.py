#would not work without the expected variables. non reusable name
def collect_unprocessed_suffixes_from_csv(path: str='') -> list:
    import os
    import csv
    if not os.path.exists(path):
        return []
    try:
        unprocessed_rows = []
        with open(path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if row.get('exists_google').strip() == '2':
                    unprocessed_rows.append(row)
        return unprocessed_rows
    except Exception as e:
        return []