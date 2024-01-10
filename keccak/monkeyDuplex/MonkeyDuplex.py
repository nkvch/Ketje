# from keccak.permutation import 
from bitarray import bitarray
from misc.padding import multi_rate_padding

class MonkeyDuplex:
    def __init__(self,f,r,n_start,n_step,n_stride):
        
        assert r > 2
        self.state = bitarray() #TODO what size?
        self.b = len(self.state)
        self.f = f
        self.r = r
        self.n_start = n_start
        self.n_step = n_step
        self.n_stride = n_stride

    def start(self,I): #I musi być bitarray
        self.state = I + multi_rate_padding(self.b,I)
        self.state = self.f(self.state)

    def step(self,o,l):
        P = o + multi_rate_padding(self.r,o)
        self.state ^= (P+(self.b-self.r) * bitarray('0'))
        self.state = self.f(self.state)

    def stride(self,o,l):
        P = o + multi_rate_padding(self.r,o)
        self.state ^= (P+(self.b-self.r) * bitarray('0'))
        self.state = self.f(self.state)