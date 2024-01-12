# from keccak.permutation import 
from bitarray import bitarray
from utils.padding import multi_rate_padding


def s_to_a(barray: bitarray, w: int) -> list:
    assert w % 8 == 0
    assert len(barray) % w == 0
    state = []
    for i in range(0, len(barray), w):
        lane = barray[i:i+w]
        lane = lane.tolist()
        state.append(lane)
    state = [state[i:i+5] for i in range(0, len(state), 5)]
    return state


def a_to_s(state: list) -> bitarray:
    assert len(state) == 5
    assert len(state[0]) == 5
    w = len(state[0][0])
    assert w % 8 == 0
    barray = bitarray()
    for lane in state:
        for row in lane:
            for bit in row:
                barray.append(bit)
    return barray


class MonkeyDuplex:
    def __init__(self,f,r,n_start,n_step,n_stride,size):
        assert r > 2
        self.state = bitarray(size)
        self.b = size
        self.w = size // 25
        self.f = f
        self.r = r
        self.n_start = n_start
        self.n_step = n_step
        self.n_stride = n_stride

    def start(self, I):
        assert len(I) <= self.b - 2
        self.state = I + multi_rate_padding(self.b, I)
        self.state = a_to_s(self.f(s_to_a(self.state, self.w), rounds = self.n_start))

    def step(self, sigma, l):
        assert l <= self.r
        assert len(sigma) <= self.r - 2
        P = sigma + multi_rate_padding(self.r,sigma)
        self.state ^= (P+(self.b-self.r) * bitarray('0'))
        self.state = a_to_s(self.f(s_to_a(self.state, self.w), rounds = self.n_step))
        Z = self.state[:l]
        return Z

    def stride(self, sigma, l):
        assert l <= self.r
        assert len(sigma) <= self.r - 2
        P = sigma + multi_rate_padding(self.r, sigma)
        self.state ^= (P+(self.b-self.r) * bitarray('0'))
        self.state = a_to_s(self.f(s_to_a(self.state, self.w), rounds = self.n_stride))
        Z = self.state[:l]
        return Z
