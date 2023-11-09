import hashlib
import json
import pandas as pd

# ___ DATA PIPELINE ___
SETTINGS = {
    'n_documents': 500,  # Max number of documents = 17
    'file_path': 'C:/Github/ID2222/code/',
    'file_name': 'eng_reviews.json'
}

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
