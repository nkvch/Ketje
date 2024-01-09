def Theta(state):
    """
    Applies the Theta step of the Keccak permutation to the given state.

    :param state: The state to be permuted, represented as a 3D array a[x][y][z].
    :return: The permuted state.
    """
    # Determine the size of the state in the z dimension
    w = len(state[0][0])
    
    # Initialize the arrays to hold the sums for each column
    C = [[0 for z in range(w)] for x in range(5)]
    D = [[0 for z in range(w)] for x in range(5)]
    
    # Calculate the sum of each column (C[x][z])
    for x in range(5):
        for z in range(w):
            for y in range(5):
                C[x][z] ^= state[x][y][z]
    
    # Calculate the D array which is used to update the state
    for x in range(5):
        for z in range(w):
            # The z-1 operation with wrap-around
            z_prev = (z - 1 + w) % w
            D[x][z] = C[(x-1) % 5][z] ^ C[(x+1) % 5][z_prev]
    
    # Update the state with the D array
    for x in range(5):
        for y in range(5):
            for z in range(w):
                state[x][y][z] ^= D[x][z]
    
    return state
