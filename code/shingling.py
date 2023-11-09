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
        for shingle in self.shingles:
            hash_value = hash(shingle)
            self.dic[shingle] = hash_value
            self.hashed_shingles.add(hash_value)
        return self.hashed_shingles
    