from bitarray import bitarray
import numpy as np

def convert_to_bitarray(val):
    bits = bitarray(val.flat())

