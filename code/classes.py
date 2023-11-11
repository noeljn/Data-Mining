import pandas as pd
import json

class DataPipeline:
    """
    Compiles document texts and their information in a pandas dataframe for easy access
    """
    def __init__(self, SETTINGS):
        self.file_path = SETTINGS['file_path']
        self.file_name = SETTINGS['file_name']
        self.n_documents = SETTINGS['n_documents']
        self.df_documents = pd.DataFrame()
        self.read_json_file()

    def read_json_file(self):
        """
        Read json file, fetch data, and then store it in a dataframe
        """
        if self.file_name == 'eng_reviews.json':
            self.df_documents = pd.DataFrame(columns=['paper_id', 'review_id', 'document_text'])
            with open(self.file_path + self.file_name) as file:
                data = json.load(file)
                for i in data['paper']:
                    for j in i['review']:
                        df_temp = pd.DataFrame(
                            {'paper_id': [i['id']], 'review_id': [j['id']], 'document_text': [j['text']]})
                        self.df_documents = pd.concat([self.df_documents, df_temp], ignore_index=True)
        elif self.file_name == 'recipes.json':
            self.df_documents = pd.DataFrame(columns=['recipe_id', 'ingredients'])
            with open(self.file_path + self.file_name) as file:
                data = json.load(file)
                for index, i in enumerate(data):
                    if index >= self.n_documents:
                        break
                    df_temp = pd.DataFrame(
                        {'recipe_id': [i['id']], 'ingredients': ' '.join(i['ingredients'])})
                    self.df_documents = pd.concat([self.df_documents, df_temp], ignore_index=True)

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