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
import ast
class AssociationRule():

    def __init__(self, frequent_sets, min_confidence, n):
        self.frequent_sets = frequent_sets
        self.min_confidence = min_confidence
        self.n = n

    def generate_rules(self):
        """
        Generate association rules from frequent itemsets.
        • Confidence (A --> B) = Support(A and B) / Support(A)
            • Confidence (1, 3 --> 4) = Support({1,3,4}) / Support({1,3})
        • Interest = P(A and B) - P(A)P(B) = Confidence - P(B)
        """
        rules = []

        for _, row in self.frequent_sets.iterrows():
            items = row['Item']
            support_itemset = row['Support']

            # Generate all possible combinations of items in the frequent itemset
            for j in range(1, len(items)):
                for antecedent in combinations(items, j):
                    antecedent = set(antecedent)    # Antecedent is a set of items
                    consequent = items - antecedent # Consequent is the rest of the items in the itemset

                    # Find the support of the antecedent and consequent
                    support_antecedent = self.frequent_sets[self.frequent_sets['Item'] == antecedent]['Support'].values[0] if antecedent else 0
                    support_consequent = self.frequent_sets[self.frequent_sets['Item'] == consequent]['Support'].values[0] if consequent else 0
        
                    # Calculate confidence
                    confidence = support_itemset / support_antecedent
                    # Confidence({1, 4}--->{2}) = Support({1,4})/Support({1,2,4}) = 2/2 = 1.0

                    # Calculate interest
                    interest = confidence - (support_consequent/self.n)
                    # Interest({1, 4}--->{2}): 1.0 - (6/7) = 0.1428571428571429 
                    
                    interest = interest if interest >= 0 else 0

                    if confidence >= self.min_confidence:
                        rules.append({'A': antecedent, 'B': consequent, 'Confidence': round(confidence,3), 'Interest': round(interest,3)})

            # • Confidence (4 --> 3) = Support({3, 4}) / Support({4})
            # • Confidence (4 --> 3) = 3 / 5 = 0.6


        return pd.DataFrame(rules)
    
    def __call__(self):
        rules = self.generate_rules()
        return rules
    
association_rule = AssociationRule(df_frequent_sets, min_confidence=0.5, n = 7)
rules = association_rule()
print(rules)



