import pandas as pd
import json
import random
import time

class Evaluation():

    def __init__(self, k, signature_size, seed, num_bands, num_buckets, SETTINGS):
        self.k = k                          # Size of shingles
        self.signature_size = signature_size    # Number of minHash signatures
        self.seed = seed                    # Seed for minHashing
        self.num_bands = num_bands          # Number of bands (sub-vectors)
        self.num_buckets = num_buckets      # Number of buckets
        self.SETTINGS = SETTINGS            # Settings   
        
    def __call__(self, df_documents):
        '''
        @param df_documents: dataframe with documents and their true similarities
        '''
        start_timer = time.time() # Start timer

        # ___ DATA PIPELINE ___
        data_pipeline = DataPipeline(self.SETTINGS)
        df_documents = data_pipeline.df_documents

        # ___ SHINGLING ___
        shingling_obj = Shingling(self.k)                   # Create shingling object with k value 
        shingling_vectors = shingling_obj(df_documents)    # Create shingling vectors

        # ___ JACCARD SIMILARITY (CompareSets) ___
        compare_sets = CompareSets()
        df_jaccard = compare_sets(shingling_vectors)        # Calculate Jaccard similarity, store in dataframe

        # ___ MINHASHING ___
        minhashing_obj = MinHashing(signature_size=self.signature_size, seed=self.seed)
        minhash_signatures= minhashing_obj(shingling_vectors)   

        # ___ COMPARE SIGNATURES (Estimate similarity) ___
        compare_signatures = CompareSignatures()
        df_estimated_similarity = compare_signatures(minhash_signatures)

        # ___ LSH ___
        lsh_obj = LSH(signature_size=self.signature_size, num_bands=self.num_bands, num_buckets=self.num_buckets)
        df_candidate_pairs = lsh_obj(minhash_signatures)

        end = time.time()
        elapsed_time = end - start_timer

        print('Elapsed time: ', elapsed_time)

# Bonus assignment           
class LSH:
    def __init__(self, signature_size, num_bands, num_buckets):
        self.signature_size = signature_size
        self.num_bands = num_bands
        self.num_buckets = num_buckets
        self.band_size = int(signature_size / num_bands)
        self.threshold = (1/num_bands)**(1/self.band_size)

    def hash(self, x):
        return hash(x) % self.num_buckets 
    
    def lsh(self, signature):
        '''
        Splits a signature into bands (sub-vectors), hashes each band, and assigns the hash values to buckets.
        '''
        buckets = [] # List of buckets
        # For each loop
        for i in range(0, self.signature_size, self.band_size):
            band = signature[i:i+self.band_size]
            buckets.append(self.hash(tuple(band))) 

        return buckets
    
    # Iterate over all buckets, check if there are any matches (i.e. candidate pairs) within the same bucket, and return all the candidate pairs
    def find_candidates(self, lsh_vec, all_lsh_vecs):
        candidate_pairs = []
        for idx, vec in enumerate(all_lsh_vecs):
            matches = 0
            for i in range(len(vec)):           # Iterate over all buckets
                if lsh_vec[i] == vec[i]:        # If there is a match, increment the number of matches
                    matches += 1
            if matches >= 1:                    # If there is at least one match, add the pair to the set of candidate pairs
                candidate_pairs.append(idx)   
        return candidate_pairs

    
    def __call__(self, df_signatures):
        '''
        Convert signatures to bands (i.e. sub-vectors), 
        then hash them and add to buckets. Each signature's bucket representation is called a "lsh vector".
        Then, we collect all lsh vectors and identify all candidate pairs, which are then collected in a dataframe.
        @param signatures: dataframe of signatures columns=['doc_id', 'signature']
        '''
        # Convert signatures to lsh vectors
        lsh_vecs = []
        for signature in df_signatures['signature']:
            lsh_vecs.append(self.lsh(signature))
        df_signatures['lsh_vec'] = lsh_vecs

        df_candidate_pairs = pd.DataFrame(columns=['id', 'candidates'])
        # Find candidate pairs
        for idx, lsh_vec in enumerate(df_signatures['lsh_vec']):
            # Remove target document from list of lsh vectors
            df_signatures_without_target = df_signatures#.drop(idx) # Drop target document from list of lsh vectors to compare
            candidate_pairs = self.find_candidates(lsh_vec, df_signatures_without_target['lsh_vec'])
            df_candidate_pairs = pd.concat([df_candidate_pairs, pd.DataFrame({'id': [idx], 'candidates': [candidate_pairs]})], ignore_index=True)

        return df_candidate_pairs

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
            self.df_documents = pd.DataFrame(columns=['doc_id', 'document_text'])
            with open(self.file_path + self.file_name) as file:
                data = json.load(file)
                for index, i in enumerate(data):
                    if index >= self.n_documents:
                        break
                    df_temp = pd.DataFrame(
                        {'doc_id': [i['id']], 'document_text': ' '.join(i['ingredients'])})
                    self.df_documents = pd.concat([self.df_documents, df_temp], ignore_index=True)

class Shingling:
    '''
    Create shingles for all documents in a given dataframe
    @param k: size of shingles
    @param shingles: set of shingles
    @param hashed_shingles: dictionary of shingles and their hash values
    '''
    def __init__(self, k):
        self.k = k

    def construct_shingles(self, document):
        shingles = set()
        for i in range(len(document) - self.k + 1):
            shingle = document[i:i+self.k]
            shingles.add(hash(shingle))

        return shingles
    
    def __call__(self, df_documents):
        '''
        Creates shingles for each document
        @param df_documents: dataframe with documents
        '''
        shingles = pd.DataFrame(columns=['doc_id', 'shingles'])
        for index, row in df_documents.iterrows():
            shingles = pd.concat([shingles, pd.DataFrame({'doc_id': [index], 'shingles': [self.construct_shingles(row['document_text'])]})], ignore_index=True)
        return shingles
    
class MinHashing:
    '''
    Represents a minHash signature of a set (S) of shingles.
    A minHash signature is a column-vector of k minHash values.
    '''
    def __init__(self, signature_size, seed, prime=4294967311):
        self.c = (2**32)-1 
        self.n = signature_size
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
    
    def hash_shingles(self, shingles):
        signature = [float('inf') for _ in range(self.n)]

        for i in range(self.n):
            for shingle in shingles:
                hash_value = self.hash_functions[i](shingle)
                signature[i] = min(signature[i], hash_value)
        return signature
    
    def __call__(self, df_shingles):
        '''
        Creates minHash signatures for each document
        @param df_shingles: dataframe with shingles
        '''
        signatures = pd.DataFrame(columns=['doc_id', 'signature'])
        for index, row in df_shingles.iterrows():
            signatures = pd.concat([signatures, pd.DataFrame({'doc_id': [index], 'signature': [self.hash_shingles(row['shingles'])]})], ignore_index=True)
        return signatures
       
class CompareSets:
    '''
    Compares two sets of shingles and calculates their Jaccard similarity
    '''
    @staticmethod

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

    def __call__(self, df_shingles):
        '''
        Calculates Jaccard similarity for each document combination
        @param df_shingles: dataframe with shingles
        '''
        df_similarity = pd.DataFrame(columns=['document1', 'document2', 'value'])
        for i in range(len(df_shingles)):
            for j in range(i+1, len(df_shingles)):
                jaccard = self.jaccard_similarity(df_shingles['shingles'][i], df_shingles['shingles'][j])
                df_similarity = pd.concat([df_similarity, pd.DataFrame({'document1': [i], 'document2': [j], 'value': [jaccard]})], ignore_index=True)
        return df_similarity

class CompareSignatures:

    @staticmethod

    def compare_signatures(signature1, signature2):
        '''
        Compares two minHash signatures and estimates their similarity
        @param signature1: minHash signature
        @param signature2: minHash signature
        @return similarity: estimated similarity between two minHash signatures
        '''
        count = 0
        for i in range(len(signature1)):
            if signature1[i] == signature2[i]:
                count += 1
        similarity = count / len(signature1)
        return similarity
    
    def __call__(self, df_signatures):
        '''
        Calculates similarity for each document combination
        @param df_signatures: dataframe with minHash signatures
        '''
        df_similarity = pd.DataFrame(columns=['document1', 'document2', 'value'])
        for i in range(len(df_signatures)):
            for j in range(i+1, len(df_signatures)):
                estimated_similarity = self.compare_signatures(df_signatures['signature'][i], df_signatures['signature'][j])
                df_similarity = pd.concat([df_similarity, pd.DataFrame({'document1': [i], 'document2': [j], 'value': [estimated_similarity]})], ignore_index=True)
        return df_similarity
    

    