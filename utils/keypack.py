from bitarray import bitarray
from bitarray.util import int2ba
from utils.padding import simple_padding

def keypack(key_bitarray: bitarray, l: int) -> bitarray:
    # enc8(l // 8) is a single byte encoding the length in bytes
    length_byte = int2ba(l // 8, length=8)
    # The key itself
    packed_key = length_byte + key_bitarray
    # Simple padding added to the key
    packed_key += simple_padding(l - 8, packed_key)
    return packed_key
