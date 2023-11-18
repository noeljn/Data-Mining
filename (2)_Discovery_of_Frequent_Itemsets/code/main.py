import pandas as pd
import numpy as np
from classes import *


SETTINGS = {
    'data_path': 'data/transactions.dat',
    'min_support': 0.01,
    'n': 100000
}

# Example usage (from: https://en.wikipedia.org/wiki/Apriori_algorithm)
dataset = Dataset(SETTINGS['data_path'], SETTINGS['n'])
print(len(dataset.data))
# Display data as a dataframe
#big_df = pd.DataFrame(columns=['Basket'])
#for _, values in data.items():
#    df_temp = pd.DataFrame({'Basket': [values]})
#    big_df = pd.concat([big_df, df_temp], axis=0, ignore_index=True)

#print(big_df)

apriori = Apriori(dataset.data, min_support=SETTINGS['min_support'], n = SETTINGS['n'], parallel=False)
#apriori = Apriori(dataset.data, min_support=2/7, n = 7, parallel=False)
df_frequent_sets, frequent_sets = apriori() # Returns a dataframe and a list of frequent sets

#print(df_frequent_sets)

association_rule = AssociationRule(frequent_sets, min_confidence=0.5, n = 7) # Returns a list of association rules
rules = association_rule()
print(rules)



