import hashlib

class Shingling:
    '''
    One Shingling-object per document
    @param k: size of shingles
    @param shingles: set of shingles
    @param hashed_shingles: dictionary of shingles and their hash values
    '''
    def __init__(self, k):
        self.k = k
        self.shingles = set()
        self.dic = {}
        self.hashed_shingles = set()

    def construct_shingles(self, document):
        for i in range(len(document) - self.k + 1):
            shingle = document[i:i+self.k]
            self.shingles.add(shingle)

    def compute_hashes(self):
        hashed_shingles = {}
        for shingle in self.shingles:
            hash_value = int(hashlib.sha256(shingle.encode('utf-8')).hexdigest(), 16)
            self.dic[shingle] = hash_value
            self.hashed_shingles.add(hash_value)
        return self.hashed_shingles
    
    
# Example Usage
document = "Lorem ipsum Lorem dolor sit amet, consectetur adipiscing elit."
k = 5  # Example k value, you can choose any value for k

shingling_obj = Shingling(k)
shingling_obj.construct_shingles(document)

hashed_shingles = shingling_obj.compute_hashes()
#print(hashed_shingles)

def jaccard_similarity(hashed_shingles_set_1, hashed_shingles_set_2):
        '''
        Calculates the Jaccard similarity between two sets of singles
        @param hashed_shingles_set_1: a set of shingles (is included in a Shingling-object)
        @param hashed_shingles_set_2: a set of shingles (is included in a Shingling-object)
        @return computed Jaccard similarity
        '''

        intersection = len(hashed_shingles_set_1.intersection(hashed_shingles_set_2))
        union = len(hashed_shingles_set_1.union(hashed_shingles_set_2))
        return intersection / union

#sim = jaccard_similarity(hashed_shingles, hashed_shingles)
#print(sim)

import random

class MinHashing:
    '''
    Represents a minHash signature of a set (S) of shingles.
    A minHash signature is a column-vector of k minHash values 
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
    
# Test
c = 100
k = 2
minhashing_obj = MinHashing(c, k, hashed_shingles)
signature = minhashing_obj.build_signature()
print(signature)
