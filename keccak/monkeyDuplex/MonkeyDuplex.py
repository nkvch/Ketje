# from keccak.permutation import 
from bitarray import bitarray
from keccak.monkeyDuplex.misc.padding import multi_rate_padding

def string_to_bitarray(string: str) -> bitarray:
    bstring = string.encode('utf-8')
    barray = bitarray()
    barray.frombytes(bstring)
    return barray

def bitarray_to_3d_array(barray: bitarray, w: int) -> list:
    # convert bitarray to 3d array of size 5x5xw
    # w is the lane size
    # assuming all lanes have the same size
    # assuming w is a multiple of 8
    assert w % 8 == 0
    assert len(barray) % w == 0
    state = []
    for i in range(0, len(barray), w):
        lane = barray[i:i+w]
        lane = lane.tolist()
        state.append(lane)
    state = [state[i:i+5] for i in range(0, len(state), 5)]
    return state


def threeD_array_to_bitarray(state: list) -> bitarray:
    # convert 3d array of size 5x5xw to bitarray
    # w is the lane size
    # assuming all lanes have the same size
    # assuming w is a multiple of 8
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
        self.state = I + multi_rate_padding(self.b, I)
        self.state = bitarray_to_3d_array(self.state, self.w)
        self.state = self.f(self.state, rounds = self.n_start)
        self.state = threeD_array_to_bitarray(self.state)


    def step(self, o, l):
        P = o + multi_rate_padding(self.r,o)
        self.state ^= (P+(self.b-self.r) * bitarray('0'))
        self.state = bitarray_to_3d_array(self.state, self.w)
        self.state = self.f(self.state, rounds = self.n_step)
        self.state = threeD_array_to_bitarray(self.state)
        Z = self.state[:l]

        return Z


    def stride(self,o,l):
        P = o + multi_rate_padding(self.r,o)
        self.state ^= (P+(self.b-self.r) * bitarray('0'))
        self.state = bitarray_to_3d_array(self.state, self.w)
        self.state = self.f(self.state,rounds = self.n_stride)
        self.state = threeD_array_to_bitarray(self.state)
        Z = self.state[:l]

        return Z
