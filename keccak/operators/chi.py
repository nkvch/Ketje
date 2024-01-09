# The Chi step is a non-linear operation applied to each row of the state array.
# For each element a[x][y], it combines that bit with two other bits in the same row:
# a[x][y] = a[x][y] ^ ((~a[x][y+1]) & a[x][y+2])

def Chi(state):
    """
    Applies the Chi step of the Keccak permutation to the given state.
    :param state: The state to be permuted, represented as a 3D array a[x][y][z].
    :return: The permuted state.
    """
    # Create a new state array to hold the results of Chi, as the operation needs to be non-destructive
    new_state = [[[0]*len(state[0][0]) for y in range(5)] for x in range(5)]
    
    # Apply the Chi transformation to each row
    for x in range(5):
        for y in range(5):
            for z in range(len(state[0][0])):
                # The bit-wise NOT operation is applied to the (y+1)th bit and then ANDed with the (y+2)th bit
                # The result is XORed with the current bit a[x][y]
                new_state[x][y][z] = state[x][y][z] ^ ((~state[x][(y+1) % 5][z]) & state[x][(y+2) % 5][z])
    
    return new_state
