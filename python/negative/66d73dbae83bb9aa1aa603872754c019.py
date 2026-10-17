def get_block_number_range(infix: str, length: int, end: str, block: int, block_size: int=500):
    infix = f'{infix}'.strip()
    end = f'{end}'.strip()
    length = int(length)
    block = int(block)
    rest = length - len(infix) - len(end)
    start_range = int(f"{infix}{rest * '0'}")
    start = start_range + block * block_size
    stop = start + block_size
    return range(int(f'{start}{end}'), int(f'{stop}{end}'))