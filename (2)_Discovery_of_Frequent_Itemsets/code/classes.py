import pandas as pd
from tqdm import tqdm
import multiprocessing as mp
import ast 
class Dataset():

    def __init__(self, data_path: str, n: int):
        self.data_path = data_path
        self.n = n
        self.data = self.load_dataset()

    def load_dataset(self):
        """
        Load a dataset from a .dat file.
        Assumes each line represents a transaction and items are separated by spaces.
        """
        dict_data = {}
        count = 0
        with open(self.data_path, 'r') as file:
            for i, line in enumerate(file):
                count += 1
                transaction = [int(item) for item in line.strip().split(' ')]
                for item in transaction:
                    if item in dict_data.keys():
                        dict_data[item].append(i)
                    else: 
                        dict_data[item] = [i]
                if count == self.n:
                    break
        
        
        return dict_data
    
from itertools import combinations

class Apriori():

    def __init__(self, baskets, min_support, parallel=True):
        self.baskets = baskets
        self.min_support = min_support
        self.parallel = parallel

    def generate_candidates(self, baskets, k):
        """
        Generate candidate itemsets of size k from a list of baskets.
        """
        candidates = set()
        
        for basket in tqdm(baskets, desc='Generating candidates for k={}'.format(k)):
            candidates.update(combinations(baskets[basket], k))   
        return candidates

    def prune_candidates(self, candidates, prev_frequent_set, k):
        """
        Prune candidates that do not have all (k-1)-subsets in the previous frequent set.
        """
        singleton_set = set()
        for e in prev_frequent_set.keys():
            singleton_set.update(e)
        pruned_candidates = set()
        for candidate in tqdm(candidates, desc='Pruning candidates for k={}'.format(k), position=0, leave=True):
            subsets = combinations(candidate, k-1)
            if all(subset in singleton_set for subset in subsets):
                pruned_candidates.add(candidate)
        return pruned_candidates
    
    def count_candidates(self, candidate, baskets, s):
        """
        Count the occurrences of candidates in a list of baskets.
        """
        intersection = set.intersection(*[set(baskets[i]) for i in candidate])
        if len(intersection) >= s:
            return {candidate: len(intersection)}
        return {}


    def apriori(self, baskets, min_support):
        """
        A-Priori algorithm for finding frequent itemsets.
        """
        #progress_bar = tqdm(desc='Main loop', leave=False)          # Progress bar
        basket_count = len(baskets) # 100,000
        s = min_support * basket_count # 1000 = 0.01 * 100,000

        k = 1   # Size of itemsets
        candidates = self.generate_candidates(baskets, k)
        print(candidates)

        while candidates:
            # Count occurrences of candidates in buckets
            if self.parallel:
                pool = mp.Pool(mp.cpu_count())
                result = pool.starmap(self.count_candidates, [(candidate, baskets, s) for candidate in candidates])
                pool.close()
            else:
                result = [self.count_candidates(candidate, baskets, s) for candidate in candidates]

            print(result)
            # Prune candidates that do not meet the minimum support
            frequent_set = {candidate: support for candidate_support in result for candidate, support in candidate_support.items()}
            print(frequent_set)
            # Generate candidates for the next iteration
            k += 1
            candidates = self.generate_candidates(baskets, k)
            candidates = self.prune_candidates(candidates, frequent_set, k)
            #progress_bar.update()   # Update progress bar
            #progress_bar.refresh()  # Refresh progress bar

        return frequent_set
    
    def __call__(self):
        frequent_sets = self.apriori(self.baskets, min_support=self.min_support)

        items_support_list = []
        for itemset in frequent_sets:
            for item, support in itemset:
                items_support_list.append({'Item': set(item) , 'Support': support})

        # Create dataframe
        df_frequent_sets = pd.DataFrame(items_support_list)
        return df_frequent_sets
    
class AssociationRule():

    def __init__(self, frequent_sets, min_confidence, n):
        self.frequent_sets = frequent_sets
        self.min_confidence = min_confidence
        self.n = n

    def generate_rules(self):
        """
        Generate association rules from frequent itemsets.
        • Confidence (A --> B) = Support(A and B) / Support(A)
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