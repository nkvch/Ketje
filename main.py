from keccak.operators.theta import Theta
from keccak.operators.rho import Rho
from keccak.operators.pi import Pi
from keccak.operators.chi import Chi
from keccak.operators.iota import Iota
from keccak.permutation import KeccakP, KeccakP_star
import numpy as np

l = 6
w = 2**l

state = np.random.randint(0, 2, (5, 5, w)).tolist()

print("Before permutation:")
print(np.array(state).reshape(w, 5, 5))

state = KeccakP_star(state)

print("After permutation:")
print(np.array(state).reshape(w, 5, 5))
