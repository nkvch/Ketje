from bitarray import bitarray     

def multi_rate_padding(r,M):
    #TODO potentially fix endianess
    bits = bitarray()
    bits.append(bitarray('1') + ((-len(M)-2)%r + 1) * bitarray('0') + bitarray('1'))
    return bits

def padding(r,M):
    #TODO potentially fix endianess
    bits = bitarray()
    bits.append(bitarray('1') + ((-len(M)-1)%r + 1) * bitarray('0'))
    return bits
