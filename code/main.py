import json
import pandas as pd
from comparesets import jaccard_similarity # Compares Jaccard similarity of two sets of hashed shingles
from shingling import Shingling
from minhashing import MinHashing
from comparesignatures import compare_signatures
from tqdm import tqdm

# ___ DATA PIPELINE ___
SETTINGS = {
    'n_documents': 250,  # Max number of documents = 17 
    'file_path': 'C:/Github/ID2222/code/',
    'file_name': 'recipes.json'
}

class DataPipeline:
    """
    Compiles document texts and their information in a pandas dataframe for easy access
    """
    def __init__(self):
        self.file_path = SETTINGS['file_path']
        self.file_name = SETTINGS['file_name']
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
                    if index >= SETTINGS['n_documents']:
                        break
                    df_temp = pd.DataFrame(
                        {'recipe_id': [i['id']], 'ingredients': ' '.join(i['ingredients'])})
                    self.df_documents = pd.concat([self.df_documents, df_temp], ignore_index=True)

# Create a DataPipeline-object
data_pipeline = DataPipeline()
print(data_pipeline.df_documents)

# > Example: Print dataframe
# print(data_pipeline.df_documents)
# > Example: Access a specific document from the dataframe
# example_text = data_pipeline.df_documents['document_text'][5]
# ------------------------------------------------------------

output = []  # List of minHash signatures
c = (2**32)-1 # Example c value, you can choose any value for c
n = 128 # Example n value, you can choose any value for n. Length of minHash signature
prime = 4294967311
minhashing_obj = MinHashing(n_signatures=n, seed=42, prime=prime)
# Create minHash signature for documents
for i in range(SETTINGS['n_documents']):
    document = data_pipeline.df_documents['ingredients'][i] # Example: document = data_pipeline.df_documents['document_text'][i]

    k = 2  # Example k value, you can choose any value for k
        
    shingling_obj = Shingling(k)
    shingling_obj.construct_shingles(document)
    shingling_obj.compute_hashes()

    signature = minhashing_obj(shingling_obj.hashed_shingles)
    output.append((signature, shingling_obj.hashed_shingles))
 
df_similarity = pd.DataFrame(columns=['document1', 'document2', 'jaccard', 'estimated_similarity'])
# Calculate Jaccard similarity and estimation of similarity
for i in tqdm(range(SETTINGS['n_documents'])):
    for j in range(i+1, SETTINGS['n_documents']):
        jaccard = jaccard_similarity(output[i][1], output[j][1])
        estimated_similarity = compare_signatures(output[i][0], output[j][0])
        
        df_similarity = pd.concat([df_similarity, pd.DataFrame({'document1': [i], 'document2': [j], 'jaccard': [jaccard], 'estimated_similarity': [estimated_similarity]})], ignore_index=True)

# Print the first 50 sorted by jaccard 
print(df_similarity.sort_values(by=['jaccard'], ascending=False).head(50))


''' K=5
       document1 document2   jaccard  estimated_similarity
15674         32       235  0.576000                   0.2
41877         92       248  0.511905                   0.1
97559        266       337  0.425806                   0.4
35842         77       423  0.403846                   0.2
25446         53       431  0.398438                   0.3
98252        269       337  0.396694                   0.4
25352         53       337  0.387597                   0.2
82038        207       274  0.354839                   0.1
117095       375       471  0.346535                   0.0
96780        262       496  0.342342                   0.2
116440       370       446  0.340694                   0.2
85527        219       337  0.336283                   0.2
10456         21       209  0.335616                   0.2
41965         92       336  0.333333                   0.3
41848         92       219  0.333333                   0.2
101181       282       367  0.331210                   0.5
85791        220       322  0.327189                   0.3
23294         49        69  0.322917                   0.0
82691        209       346  0.320988                   0.2
22660         47       336  0.318966                   0.3
16526         34       156  0.317460                   0.3
6059          12       150  0.317164                   0.1
85921        220       452  0.316667                   0.3
36606         79       346  0.315789                   0.0
22416         47        92  0.315385                   0.3
6299          12       390  0.315353                   0.3
25284         53       269  0.315068                   0.1
13675         28       110  0.314516                   0.3
36469         79       209  0.314103                   0.3
85459        219       269  0.312000                   0.1
21435         44       470  0.311404                   0.2
10593         21       346  0.309524                   0.3
42109         92       480  0.308725                   0.2
90396        237       337  0.308081                   0.3
36242         78       402  0.304348                   0.3
86225        221       478  0.303797                   0.3
92992        247       368  0.302013                   0.3
62794        147       320  0.301508                   0.3
10326         21        79  0.300000                   0.2
20277         42       223  0.298507                   0.5
102642       289       337  0.298507                   0.3
82599        209       254  0.298182                   0.3
121729       421       482  0.296703                   0.2
111580       337       371  0.295455                   0.4
85670        219       480  0.295302                   0.2
50746        114       416  0.293333                   0.1
112789       344       474  0.290323                   0.4
25111         53        96  0.288770                   0.2
101076       281       479  0.288462                   0.3
111502       336       455  0.287500                   0.1

'''