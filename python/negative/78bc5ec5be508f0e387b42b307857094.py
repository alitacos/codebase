#works but is prefered using better type hints or defaults, output hints, maybe exception handling
# the function is very unique for a spesific case... without the archives we can not test
# is missing password functionality and handling
#non reusable

def process_archives_in_mounted_drive_in_wsl_to_extract_cc_logs_from_q(drive: str=None, filepath: str=None, querypath: str=None, outputfile: str=None, last_counter: int=0):

    def collect_startpaths_of_archives_from_mounted_drive_to_index_file(drive: str=None, index: str=None):

        def write_output(filename=None, data=None):
            with open(filename, 'a') as f:
                for i in data:
                    f.write(i + '\n')
                print('data successfully stored in ' + filename)
        import glob
        source_path = '/mnt/' + drive
        q = glob.glob(source_path + '/**/*.rar', recursive=True)
        write_output(filename=index, data=q)

    def get_archive_from_index(filepath=None):
        import rarfile

        def open_archive_obj(path: str) -> str:
            try:
                archive = rarfile.RarFile(path, mode='r')
                return archive
            except rarfile.BadRarFile:
                return None
        with open(filepath, 'r') as f:
            data = f.read().split('\n')
            firstline = data[0] if data else None
            return open_archive_obj(firstline)

    def remove_archive_from_index(filepath=None):
        with open(filepath, 'r') as file:
            lines = file.readlines()
        if lines:
            lines = lines[1:]
        with open(filepath, 'w') as file:
            for line in lines:
                if line:
                    file.write(line.strip() + '\n')

    def get_cc_logs(item, file):
        try:
            with item.open(file, 'r') as f:
                data = []
                datalist = iter(f.read().decode().split('\n'))
                for line in datalist:
                    if line.lower().startswith('holder'):
                        holder = line
                        cctype = next(datalist)
                        cardnr = next(datalist)
                        if holder.lower().startswith('holder') and cctype.lower().startswith('cardtype') and cardnr.lower().startswith('card'):
                            data.append({'holder': ':'.join(holder.split(':')[1:]).strip(), 'cardtype': ':'.join(cctype.split(':')[1:]).strip(), 'card_id': ':'.join(cardnr.split(':')[1:]).strip()})
                f.close()
                return data
        except Exception:
            return []

    def storelogs(obj, path):
        try:
            with open(path, 'r') as f:
                totals = f.read().splitlines()
        except Exception as s:
            print(str(s))
            totals = []
        with open(path, 'a+') as f:
            if obj:
                for i in obj:
                    if i not in totals:
                        f.write(str(i) + '\n')

    def get_set(path):
        try:
            with open(path, 'r') as f:
                rd = f.read().split('\n')
                gset = sorted(set(rd))
                return gset
                print(len(rd), len(gset))
        except Exception as e:
            print(str(e))

    def remove_doubles(path):
        gset = get_set(path)
        try:
            with open(path, 'w') as f:
                for line in gset:
                    f.write(line + '\n')
        except Exception as e:
            print(str(e))
    start_paths = collect_startpaths_of_archives_from_mounted_drive_to_index_file(drive='d', index=filepath)
    archive = get_archive_from_index(filepath=filepath)
    fcounter = last_counter
    while archive:
        print(archive.filename)
        rm = remove_archive_from_index(filepath=filepath)
        namelist = archive.namelist()
        ccfiles = [i for i in namelist if querypath in i.lower() and i.endswith('.txt')]
        counter = len(ccfiles)
        print(counter)
        logcount = 0
        for file in ccfiles:
            logs = get_cc_logs(archive, file)
            logcount += len(logs)
            store = storelogs(logs, outputfile + str(fcounter) + '.txt')
        del namelist
        del ccfiles
        print(archive.filename, counter, logcount)
        close = archive.close()
        redouble = remove_doubles(outputfile + str(fcounter) + '.txt')
        del archive
        archive = get_archive_from_index(filepath=filepath)
        fcounter += 1