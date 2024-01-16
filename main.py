import Ketje
from bitarray import bitarray

if __name__ == "__main__":

    A = bitarray('0' * 64)
    B = bitarray('1' * 64)
    K = bitarray('0' * 64)
    N = bitarray('0' * 32)
    Ketje.enc(A, B, K, N)
    print(Ketje.enc(A, B, K, N))
