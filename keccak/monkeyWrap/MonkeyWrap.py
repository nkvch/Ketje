from bitarray import bitarray

def concat_int_with(bit: int, str_bitarray: str) -> bitarray:
    return bitarray(str(bit) + str_bitarray)

class MonkeyWrap:
    def __init__(self, monkey_duplex):
        self.duplex = monkey_duplex

    def initialize(self, K, N):
        # Initialize the MonkeyDuplex with the key and nonce
        # The key is assumed to be a bitarray
        key_bit_length = len(K) * 8
        key_length_bits = bitarray(format(key_bit_length, '016b'))  # Represent the key length in 16 bits
        keypack = K + key_length_bits
        self.duplex.start(keypack + N)

    def wrap(self, A, B, l):
        # Process the header A
        for i in range(len(A) - 1):
            # concat A[i] with 00
            self.duplex.step(A[i] + bitarray('00'), 0)
        Z = self.duplex.step(A[-1] + bitarray('01'), len(B[0]))

        # Process the body B
        C = []
        C0 = B[0] ^ Z
        C.append(C0)

        for i in range(0, len(B) - 1):
            Z = self.duplex.step(B[i], len(B[i+1]))
            Ci_plus_1 = B[i+1] ^ Z
            C.append(Ci_plus_1)

        # Generate the tag T
        T = self.duplex.stride(B[-1] + bitarray('10'), l)

        while len(T) < l:
            T += self.duplex.stride(bitarray(0), l)

        T = T[:l]

        return C, T

    def unwrap(self, A, C, T):
        # Process the header A
        for i in range(len(A) - 1):
            self.duplex.step(A[i] + bitarray('00'), 0)
        Z = self.duplex.step(A[-1] + bitarray('01'), len(C[0]))

        # Process the cryptogram C
        B = []
        B0 = C[0] ^ Z
        B.append(B0)

        for i in range(0, len(C) - 1):
            Z = self.duplex.step(B[i] + bitarray('11'), len(C[i+1]))
            Bi_plus_1 = C[i+1] ^ Z
            B.append(Bi_plus_1)

        # Generate the verification tag T_prime and compare with T
        T_prime = self.duplex.stride(B[len(C) - 1] + bitarray('10'), len(T))

        while len(T_prime) < len(T):
            T_prime += self.duplex.stride(bitarray(0), len(T))

        if T_prime != T:
            raise ValueError("Authentication failed.")

        return B
