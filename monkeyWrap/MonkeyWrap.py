from bitarray import bitarray
from typing import List

from utils.keypack import keypack

def concat_int_with(bit: int, str_bitarray: str) -> bitarray:
    return bitarray(str(bit) + str_bitarray)

class MonkeyWrap:
    def __init__(self, monkey_duplex, rho):
        self.duplex = monkey_duplex
        self.rho = rho

    def initialize(self, K, N):
        # Initialize the MonkeyDuplex with the key and nonce
        # The key is assumed to be a bitarray
        assert len(K) <= self.duplex.b - 18
        assert len(N) <= self.duplex.b - len(K) - 18

        self.duplex.start(keypack(K, len(K) + 16) + N)

    def blocks(self, barray: bitarray) -> (List[bitarray], int):
        is_empty = len(barray) == 0
        if is_empty:
            return [bitarray('')], 1
        
        blocks = []
        for i in range(0, len(barray), self.rho):
            blocks.append(barray[i:i+self.rho])

        return blocks, len(blocks)
    
    def from_blocks(self, blocks: List[bitarray]) -> bitarray:
        barray = bitarray()
        for block in blocks:
            barray += block
        return barray

    def wrap(self, A, B, l):
        assert type(A) == bitarray
        assert type(B) == bitarray
        assert l >= 0

        A_blocks, A_blocks_len = self.blocks(A)
        B_blocks, B_blocks_len = self.blocks(B)

        for i in range(A_blocks_len - 1):
            self.duplex.step(A_blocks[i] + bitarray('00'), 0)

        Z = self.duplex.step(A_blocks[-1] + bitarray('01'), len(B_blocks[0]))

        C_blocks = []
        C0_block = B_blocks[0] ^ Z
        C_blocks.append(C0_block)

        for i in range(0, B_blocks_len - 1):
            Z = self.duplex.step(B_blocks[i] + bitarray('11'), len(B_blocks[i+1]))
            Ci_plus_1_block = B_blocks[i+1] ^ Z
            C_blocks.append(Ci_plus_1_block)

        C = self.from_blocks(C_blocks)

        T = self.duplex.stride(B_blocks[-1] + bitarray('10'), self.rho)

        while len(T) < l:
            T += self.duplex.stride(bitarray(0), self.rho)

        T = T[:l]

        assert len(T) == l

        return C, T

    def unwrap(self, A, C, T):
        assert type(A) == bitarray
        assert type(C) == bitarray
        assert type(T) == bitarray

        A_blocks, A_blocks_len = self.blocks(A)
        C_blocks, C_blocks_len = self.blocks(C)

        for i in range(A_blocks_len - 1):
            self.duplex.step(A_blocks[i] + bitarray('00'), 0)
        
        Z = self.duplex.step(A_blocks[-1] + bitarray('01'), len(C_blocks[0])) # length of C0 is the same as length of B0

        B_blocks = []
        B0_block = C_blocks[0] ^ Z
        B_blocks.append(B0_block)

        for i in range(0, C_blocks_len - 1):
            Z = self.duplex.step(B_blocks[i] + bitarray('11'), len(C_blocks[i+1]))
            Bi_plus_1_block = C_blocks[i+1] ^ Z
            B_blocks.append(Bi_plus_1_block)

        T_prime = self.duplex.stride(B_blocks[C_blocks_len - 1] + bitarray('10'), self.rho)

        while len(T_prime) < len(T):
            T_prime += self.duplex.stride(bitarray(0), self.rho)

        T_prime = T_prime[:len(T)]

        if T_prime != T:
            raise ValueError("Authentication failed.")

        return self.from_blocks(B_blocks)
