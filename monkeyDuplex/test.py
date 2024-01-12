import unittest
from bitarray import bitarray
from monkeyDuplex.MonkeyDuplex import MonkeyDuplex, s_to_a, a_to_s

class TestMonkeyDuplex(unittest.TestCase):
    def setUp(self):
        # Initialize with a dummy permutation function that just returns the state
        self.dummy_permutation = lambda state, rounds: state
        self.r = 8  # Rate for the duplex, just an example
        self.b = 1600  # State size, for Keccak-f[1600]
        self.monkey_duplex = MonkeyDuplex(self.dummy_permutation, self.r, 12, 1, 2, self.b)

    def test_s_to_a_a_to_s(self):
        original_state = bitarray('1' * self.b)
        state_a = s_to_a(original_state, self.monkey_duplex.w)
        state_s = a_to_s(state_a)
        self.assertEqual(original_state, state_s, "Conversion between state representations should be lossless")

    def test_step(self):
        # Test the step function with some input
        input_sigma = bitarray('1100')
        output_length = 4
        Z = self.monkey_duplex.step(input_sigma, output_length)
        self.assertEqual(len(Z), output_length, "Step should output the correct number of bits")