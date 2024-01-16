from keccak.permutation import KeccakP_star
from monkeyDuplex.MonkeyDuplex import MonkeyDuplex
from monkeyWrap.MonkeyWrap import MonkeyWrap
from bitarray import bitarray

def enc(A,B,K= bitarray('0' * 64),N= bitarray('0' * 32)):

    b = 200  # State size for Keccak-f[200]
    r = 22
    rho = 16
    n_start, n_step, n_stride = 12, 1, 6  # Round parameters
    l = 64  # Tag length

    KetjeJR_MonkeyDuplex = MonkeyDuplex(KeccakP_star, r, n_start, n_step, n_stride, b)
    KetjeJR = MonkeyWrap(KetjeJR_MonkeyDuplex, rho)
    KetjeJR.initialize(K, N)



    A1, B1 = KetjeJR.wrap(A, B, l)

    KetjeJR2_MonkeyDuplex = MonkeyDuplex(KeccakP_star, r, n_start, n_step, n_stride, b)
    KetjeJR2 = MonkeyWrap(KetjeJR2_MonkeyDuplex, rho)
    KetjeJR2.initialize(K, N)

    A2, B2 = KetjeJR.wrap(A1, B1, l)

    KetjeJR3_MonkeyDuplex = MonkeyDuplex(KeccakP_star, r, n_start, n_step, n_stride, b)
    KetjeJR3 = MonkeyWrap(KetjeJR3_MonkeyDuplex, rho)
    KetjeJR3.initialize(K, N)

    A3, B3 = KetjeJR.wrap(A2, B2, l)

    KetjeJR4_MonkeyDuplex = MonkeyDuplex(KeccakP_star, r, n_start, n_step, n_stride, b)
    KetjeJR4 = MonkeyWrap(KetjeJR4_MonkeyDuplex, rho)
    KetjeJR4.initialize(K, N)

    A4, B4 = KetjeJR.wrap(A3, B3, l)

    return A4, B4

