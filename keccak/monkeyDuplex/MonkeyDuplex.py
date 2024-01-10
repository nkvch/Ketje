# from keccak.permutation import 
from bitarray import bitarray
from misc.padding import multi_rate_padding

class MonkeyDuplex:
    def __init__(self,f,r,n_start,n_step,n_stride,size):
        
        assert r > 2
        self.state = bitarray(size)
        self.b = size
        self.f = f
        self.r = r
        self.n_start = n_start
        self.n_step = n_step
        self.n_stride = n_stride

    def start(self,I): #I musi być bitarray
        self.state = I + multi_rate_padding(self.b,I)
        self.state = self.f(self.state, rounds = self.n_start)

    def step(self,o,l):
        P = o + multi_rate_padding(self.r,o)
        self.state ^= (P+(self.b-self.r) * bitarray('0'))
        self.state = self.f(self.state, rounds = self.n_step)

    def stride(self,o,l):
        P = o + multi_rate_padding(self.r,o)
        self.state ^= (P+(self.b-self.r) * bitarray('0'))
        self.state = self.f(self.state,rounds = self.n_stride)