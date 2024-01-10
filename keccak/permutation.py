from keccak.operators.theta import Theta
from keccak.operators.rho import Rho
from keccak.operators.pi import Pi, Pi_inv
from keccak.operators.chi import Chi
from keccak.operators.iota import Iota


def KeccakP(state, rounds=24):
    for i in range(rounds):
        state = Theta(state)
        state = Rho(state)
        state = Pi(state)
        state = Chi(state)
        state = Iota(state, i)
    return state


def KeccakP_star(state, rounds=24):
    state = Pi_inv(state)
    state = KeccakP(state, rounds)
    state = Pi(state)
    return state
