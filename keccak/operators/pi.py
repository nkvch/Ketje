# The Pi step is a permutation of the lanes in the state. Each lane a[x, y] is moved to a new position a[x', y'].
# The new positions (x', y') are determined by multiplying the matrix ((0 1), (2 3)) with the vector (x, y) over GF(5).

# Define the function to perform the matrix multiplication over GF(5)
def matrix_multiply_GF5(matrix, vector):
    # Perform matrix multiplication modulo 5
    x, y = vector
    x_prime = (matrix[0][0] * x + matrix[0][1] * y) % 5
    y_prime = (matrix[1][0] * x + matrix[1][1] * y) % 5
    return (x_prime, y_prime)

def Pi(state):
    """
    Applies the Pi step of the Keccak permutation to the given state.
    :param state: The state to be permuted, represented as a 3D array a[x][y][z].
    :return: The permuted state.
    """
    # Create a new empty state to hold the permuted lanes
    new_state = [[[0]*len(state[0][0]) for _ in range(5)] for _ in range(5)]
    
    # Define the matrix used for the Pi step
    matrix = [[0, 1], [2, 3]]
    
    # Apply the Pi transformation to each lane
    for x in range(5):
        for y in range(5):
            # Calculate the new positions using the matrix multiplication over GF(5)
            x_prime, y_prime = matrix_multiply_GF5(matrix, (x, y))
            
            # Move the entire lane (all z values) to the new position
            for z in range(len(state[0][0])):
                new_state[x_prime][y_prime][z] = state[x][y][z]
    
    return new_state


def Pi_inv(state):
    """
    Applies the inverse of the Pi step of the Keccak permutation to the given state.
    :param state: The state to be permuted, represented as a 3D array a[x][y][z].
    :return: The permuted state.
    """
    # Create a new empty state to hold the permuted lanes
    new_state = [[[0]*len(state[0][0]) for _ in range(5)] for _ in range(5)]
    
    # Define the inverse matrix used for the Pi step
    matrix_inv = [[1, 3], [1, 0]]

    # Apply the inverse Pi transformation to each lane
    for x in range(5):
        for y in range(5):
            # Calculate the new positions using the matrix multiplication over GF(5)
            x_prime, y_prime = matrix_multiply_GF5(matrix_inv, (x, y))
            
            # Move the entire lane (all z values) to the new position
            for z in range(len(state[0][0])):
                new_state[x_prime][y_prime][z] = state[x][y][z]

    return new_state
