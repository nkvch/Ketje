from keccak.operators.theta import Theta
from keccak.operators.rho import Rho
from keccak.operators.pi import Pi
from keccak.operators.chi import Chi
from keccak.operators.iota import Iota
from keccak.permutation import KeccakP, KeccakP_star
import numpy as np
from keccak.monkeyDuplex.MonkeyDuplex import MonkeyDuplex
from keccak.monkeyWrap.MonkeyWrap import MonkeyWrap
from bitarray import bitarray

D = MonkeyDuplex(KeccakP, r=1024, n_start=24, n_step=24, n_stride=24, size=1600)

W = MonkeyWrap(D)

key = bitarray('1010101010101010101010101010101010101010101010101010101010101010')
nonce = bitarray('1010101010101010101010101010101010101010101010101010101010101010')

W.initialize(key, nonce)

A = [
    bitarray('1010101010101010101010101010101010101010101010101010101010101010'),
    bitarray('1010101010101010101010101010101010101010101010101010101010101010')
]

B = [
    bitarray('1010101010101010101010101010101010101010101010101010101010101010'),
    bitarray('1010101010101010101010101010101010101010101010101010101010101010')
]

tag_length = 1024

cryptogram, tag = W.wrap(A, B, tag_length)

print(cryptogram)
print(tag)


B_prime = W.unwrap(A, cryptogram, tag)
