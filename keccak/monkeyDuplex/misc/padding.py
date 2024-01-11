from bitarray import bitarray     

def multi_rate_padding(r, M):
    pad_len = (-len(M)-2) % r #+ 1
    padding = bitarray('1') + pad_len * bitarray('0') + bitarray('1')
    return padding

def padding(r, M):
    pad_len = (-len(M)-1) % r #+ 1
    padding = bitarray('1') + pad_len * bitarray('0')
    return padding
