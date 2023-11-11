
from classes import DataPipeline, Shingling, CompareSets, MinHashing, CompareSignatures, LSH


# ___ DATA PIPELINE ___
SETTINGS = {
    'n_documents': 20,  # Max number of documents = 17 
    'file_path': 'C:/Github/ID2222/data/',
    'file_name': 'recipes.json'
}

# ___ DATA PIPELINE ___
data_pipeline = DataPipeline(SETTINGS)
df_documents = data_pipeline.df_documents

# ___ SHINGLING ___
k = 2
shingling_obj = Shingling(k)                   # Create shingling object with k value 
shingling_vectors = shingling_obj(df_documents)    # Create shingling vectors

# ___ JACCARD SIMILARITY (CompareSets) ___
#compare_sets = CompareSets()
#df_jaccard = compare_sets(shingling_vectors)        # Calculate Jaccard similarity, store in dataframe
# Print top 10 most similar documents
#print(df_jaccard.sort_values(by='jaccard_similarity', ascending=False).head(10))

# ___ MINHASHING ___
n = 125
seed = 42
minhashing_obj = MinHashing(signature_size=n, seed=seed)
minhash_signatures= minhashing_obj(shingling_vectors)   

# ___ COMPARE SIGNATURES (Estimate similarity) ___
compare_signatures = CompareSignatures()
print(compare_signatures(minhash_signatures))
#df_estimated_similarity = compare_signatures(minhash_signatures)
#print(df_estimated_similarity.sort_values(by='estimated_similarity', ascending=False).head(10))

# ___ LSH ___
num_bands = 5       # Number of bands (sub-vectors) to divide a signature into
num_buckets = 25
band_size = int(n / num_bands)
threshold = (1/num_bands)**(1/band_size)
lsh_obj = LSH(signature_size=n, num_bands=num_bands, num_buckets=num_buckets)
print(lsh_obj.threshold)
df_candidate_pairs = lsh_obj(minhash_signatures)
print(df_candidate_pairs)

# ___ PRINT RESULTS ___