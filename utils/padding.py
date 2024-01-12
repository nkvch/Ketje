from bitarray import bitarray

def multi_rate_padding(r, M):
    # Calculate the number of zero bits needed, and account for the '1' at the start and end.
    pad_len = (-len(M) - 2) % r
    padding = bitarray('1') + pad_len * bitarray('0') + bitarray('1')
    return padding

def simple_padding(r, M):
    # Calculate the number of zero bits needed, and account for the '1' at the start.
    pad_len = (-len(M) - 1) % r
    padding = bitarray('1') + pad_len * bitarray('0')
    return padding
