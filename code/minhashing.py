import random
from typing import Any

class MinHashing:
    '''
    Represents a minHash signature of a set (S) of shingles.
    A minHash signature is a column-vector of k minHash values.
    '''
    def __init__(self, n_signatures, seed, prime):
        self.c = (2**32)-1 
        self.n = n_signatures
        self.seed = seed
        self.prime = prime
        self.hash_functions = [self.generate_hash_functions() for _ in range(self.n)]

    def generate_hash_functions(self):
        '''
        Generate hash function
        '''
        random.seed(self.seed)
        a = random.randint(1, self.c)
        random.seed(self.seed+1)
        b = random.randint(1, self.c)
        self.seed += 2
        return lambda x: (a*x + b) % self.prime
    
    
    def __call__(self, shingles):
        signature = [float('inf') for _ in range(self.n)]

        for i in range(self.n):
            for shingle in shingles:
                hash_value = self.hash_functions[i](shingle)
                signature[i] = min(signature[i], hash_value)
        return signature