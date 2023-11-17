import pandas as pd
from classes import *


SETTINGS = {
    'data_path': 'data/transactions.dat',
    'min_support': 0.01,
    'n': 10000
}

# Load dataset
dataset = Dataset(SETTINGS['data_path'], SETTINGS['n'])
print(dataset.df_data)

# Example usage (from: https://en.wikipedia.org/wiki/Apriori_algorithm)
data = [
    '1 2 3 4',
    '1 2 4',
    '1 2',
    '2 3 4',
    '2 3',
    '3 4',
    '2 4'
]

df_data = pd.DataFrame(data, columns=['Baskets'])
print(df_data)

#apriori = Apriori(dataset.df_data['Baskets'], min_support=SETTINGS['min_support'])
apriori = Apriori(df_data['Baskets'], min_support=2/7)
df_frequent_sets = apriori()

print(df_frequent_sets)

association_rule = AssociationRule(df_frequent_sets, min_confidence=0.5, n = 7)
rules = association_rule()
print(rules)



