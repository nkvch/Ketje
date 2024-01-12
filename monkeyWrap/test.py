import unittest
from bitarray import bitarray
from monkeyDuplex.MonkeyDuplex import MonkeyDuplex, s_to_a, a_to_s
from monkeyWrap.MonkeyWrap import MonkeyWrap
from keccak.permutation import KeccakP

class TestMonkeyWrap(unittest.TestCase):

    def setUp(self):
        # Parameters for MonkeyDuplex
        b = 1600  # State size for Keccak-f[1600]
        rho = 8
        n_start, n_step, n_stride = 12, 1, 2  # Round parameters

        # Initialize the MonkeyDuplex and MonkeyWrap
        self.monkey_duplex = MonkeyDuplex(KeccakP, rho + 4, n_start, n_step, n_stride, b)
        self.monkey_wrap = MonkeyWrap(self.monkey_duplex, rho)

    def test_initialization(self):
        K = bitarray('0' * 128)  # 128-bit key
        N = bitarray('0' * 128)  # 128-bit nonce
        self.monkey_wrap.initialize(K, N)
        # The state should not be all zeros after initialization
        self.assertNotEqual(self.monkey_wrap.duplex.state, bitarray('0' * 1600))

    def test_wrap_and_unwrap(self):
        # Use a fixed key and nonce for testing
        K = bitarray('0' * 128)  # 128-bit key
        N = bitarray('0' * 128)  # 128-bit nonce
        self.monkey_wrap.initialize(K, N)

        # Header and body for wrapping
        A = bitarray('0' * 64)  # 64-bit header
        B = bitarray('1' * 64)  # 64-bit body
        l = 64  # Tag length

        # Wrap the header and body
        C, T = self.monkey_wrap.wrap(A, B, l)
        
        # Unwrap should recover the original body
        B_recovered = self.monkey_wrap.unwrap(A, C, T)
        self.assertEqual(B, B_recovered)

    # More unit tests would be written for other cases and edge conditions.

if __name__ == '__main__':
    unittest.main()
