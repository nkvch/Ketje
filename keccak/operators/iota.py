def Iota(state, round_index):
    """
    Applies the Iota step of the Keccak permutation to the given state.
    :param state: The state to be permuted, represented as a 3D array a[x][y][z].
    :param round_index: The index of the current round (i_r).
    :return: The permuted state.
    """
    # Define the round constants for Keccak-f[1600]
    # This is a simplified representation; the actual RC values would need to be generated according to the specification.
    RC = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
        0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
        0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
        0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
        0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
        0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
        0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
        0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]

    # Convert the 64-bit round constant to its binary representation
    RC_bin = [int(b) for b in format(RC[round_index], '064b')]

    # XOR the round constant with the first lane of the state
    for z in range(64):
        state[0][0][z] ^= RC_bin[z]

    return state
