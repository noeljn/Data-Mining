import random

class MinHashing:
    '''
    Represents a minHash signature of a set (S) of shingles.
    A minHash signature is a column-vector of k minHash values.
    '''
    def __init__(self, c, k, hashed_shingles):
        self.hashed_shingles = hashed_shingles
        self.c = c 
        self.k = k
        self.hash_functions = [self.generate_hash_functions() for _ in range(k)]

    def generate_hash_functions(self):
        '''
        Generate hash function
        '''
        a = random.randint(1, self.c)
        b = random.randint(0, self.c)
        return lambda x: (a*x + b) % self.c 
    
    def build_signature(self):
        signature = [float('inf') for _ in range(self.k)]

        for i in range(self.k):
            for shingle in self.hashed_shingles:
                hash_value = self.hash_functions[i](shingle)
                signature[i] = min(signature[i], hash_value)
        return signature