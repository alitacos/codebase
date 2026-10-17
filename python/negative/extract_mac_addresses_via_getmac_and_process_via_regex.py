def extract_mac_addresses_via_getmac_and_process_via_regex(): # did not work as expected. returns FileNotFoundError
    """
    Retrieves MAC addresses and transport names using the `getmac` command.

    Returns:
        List of tuples containing MAC addresses and transport names.
    """
    import subprocess
    import re
    #import  winreg
    mac_addresses = []
    getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode().split('\n')
    macAddRegex = re.compile(r'(?:[0-9a-fA-F]:?){12}')
    transportName = re.compile(r'(Transport\s*\d{1,})')

    for macAdd in getmac_output:
        macFind = macAddRegex.search(macAdd)
        transportFind = transportName.search(macAdd)
        if macFind and transportFind:
            mac_addresses.append((macFind.group(0), transportFind.group(0)))
    return mac_addresses
# Example Usage:
#mac_addresses = extract_mac_addresses_via_getmac_and_process_via_regex()
#out: FileNotFoundError: [Errno 2] No such file or directory: 'getmac'
