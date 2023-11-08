import hashlib
import json
import pandas as pd

# ___ SETTINGS ___
SETTINGS = {
    'n_documents': 10,
    'file_path': 'C:/Users/alexa/OneDrive/KTH grejer/ID2222 Data Mining/Lab assignments/Lab 1/',
    'file_name': 'eng_reviews.json'
}

# ___ DATA PIPELINE ___
class DataPipeline:
    """
    Compiles document texts and their information in a pandas dataframe for easy access
    """
    def __init__(self):
        self.file = SETTINGS['file_path'] + SETTINGS['file_name']
        self.df_documents = pd.DataFrame(columns=['paper_id', 'review_id', 'document_text'])
        self.read_json_file()

    def read_json_file(self):
        """
        Read json file, fetch data, and then store it in a dataframe
        """
        with open(self.file) as file:
            data = json.load(file)
            for i in data['paper']:
                for j in i['review']:
                    df_temp = pd.DataFrame(
                        {'paper_id': [i['id']], 'review_id': [j['id']], 'document_text': [j['text']]})
                    self.df_documents = pd.concat([self.df_documents, df_temp], ignore_index=True)


# Create a DataPipeline-object
data_pipeline = DataPipeline()
print(data_pipeline.df_documents)

# > Example: Print dataframe
# print(data_pipeline.df_documents)
# > Example: Access a specific document from the dataframe
# example_text = data_pipeline.df_documents['document_text'][5]
# ------------------------------------------------------------

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
    
# Test
c = 100
k = 2
minhashing_obj = MinHashing(c, k, hashed_shingles)
signature = minhashing_obj.build_signature()
#print(signature)

def compare_signatures(signature1, signature2):
    '''
    Compares two minHash signatures and calculates the similarity
    @param signature1: minHash signature
    @param signature2: minHash signature
    @return similarity: similarity between two minHash signatures
    '''
    count = 0
    for i in range(len(signature1)):
        if signature1[i] == signature2[i]:
            count += 1
    similarity = count / len(signature1)
    return similarity

# Test
signature1 = [1, 4, 2]
signature2 = [1, 2, 2]
similarity = compare_signatures(signature1, signature2)
print(similarity)




