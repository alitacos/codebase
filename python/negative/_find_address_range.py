

def _find_address_range(addresses):
    """Find a sequence of sorted deduplicated IPv#Address.
    
    Args:
        addresses: a list of IP address strings (IPv4 or IPv6).
    
    Yields:
        A tuple containing the first and last IP addresses in the sequence.
    """
    # Convert IP addresses to ipaddress objects and sort them
     
    # Initialize the first and last IP addresses
    it = iter(addresses)
    first = last = next(it)
    
    # Iterate over the addresses
    for ip in it:
        if ip != last + 1:
            yield str(first), str(last)
            first = ip
        last = ip
    
    # Yield the final range
    yield str(first), str(last)

# Test with a list of IP addresses
addresses = [
    '192.168.1.1',
    '192.168.1.2',
    '192.168.1.3',
    '192.168.1.5',
    '192.168.1.6',
    '192.168.1.1',
    '192.168.1.2',
    '192.168.1.3',
    '192.168.1.5',
    '192.168.1.6'

]

# Calling the function and printing the result
for start, end in _find_address_range(addresses):
    print(f"{start} - {end}")
