import pandas as pd
from tqdm import tqdm

class Dataset():

    def __init__(self, data_path: str, n: int):
        self.data_path = data_path
        self.n = n
        self.df_data = self.load_dataset()
        

    def load_dataset(self):
        """
        Load a dataset from a .dat file.
        Assumes each line represents a transaction and items are separated by spaces.
        """
        
        with open(self.data_path, 'r') as file:
            # Read only the first n lines
            lines = file.readlines()[:self.n]
            transactions = [line.strip() for line in lines]
        
        df = pd.DataFrame(transactions, columns=['Baskets'])

        return df
    
from itertools import combinations

class Apriori():

    def __init__(self, baskets, min_support):
        self.baskets = [basket.split() for basket in baskets.values]
        self.min_support = min_support

    def generate_candidates(self, baskets, k):
        """
        Generate candidate itemsets of size k from a list of baskets.
        """
        candidates = set()
        
        for basket in tqdm(baskets, desc='Generating candidates for k={}'.format(k)):
            candidates.update(combinations(basket, k))
        return candidates

    def prune_candidates(self, candidates, prev_frequent_set, k):
        """
        Prune candidates that do not have all (k-1)-subsets in the previous frequent set.
        """
        pruned_candidates = set()
        for candidate in tqdm(candidates, desc='Pruning candidates for k={}'.format(k), position=0, leave=True):
            subsets = combinations(candidate, k-1)
            if all(subset in prev_frequent_set for subset in subsets):
                pruned_candidates.add(candidate)
        return pruned_candidates

    #def generator(self, baskets, min_support):
    #    while True:
    #        yield 

    #for _ in tqdm(generator(baskets, min_support)):


    def apriori(self, baskets, min_support):
        """
        A-Priori algorithm for finding frequent itemsets.
        """
        progress_bar = tqdm(desc='Main loop', leave=False)          # Progress bar
        basket_count = len(baskets) # 100,000
        s = min_support * basket_count # 1000 = 0.01 * 100,000

        # Initialize frequent itemsets
        frequent_sets = []
        k = 1   # Size of itemsets
        candidates = self.generate_candidates(baskets, k)

        while candidates:
            # Count occurrences of candidates in buckets
            candidate_counts = {candidate: 0 for candidate in candidates}
            for basket in tqdm(baskets, desc='Counting candidates for k={}'.format(k), leave=False):
                for candidate in candidates:
                    if set(candidate).issubset(basket):
                        candidate_counts[candidate] += 1

            # Prune candidates that do not meet the minimum support
            frequent_set = {candidate for candidate, count in candidate_counts.items() if count >= s}
            frequent_sets.append({(candidate, count) for candidate, count in candidate_counts.items() if count >= s})
            
            # Generate candidates for the next iteration
            k += 1
            candidates = self.generate_candidates(baskets, k)
            candidates = self.prune_candidates(candidates, frequent_set, k)
            progress_bar.update()   # Update progress bar
            progress_bar.refresh()  # Refresh progress bar

        return frequent_sets
    
    def __call__(self):
        frequent_sets = self.apriori(self.baskets, min_support=self.min_support)

        items_support_list = []
        for itemset in frequent_sets:
            for item, support in itemset:
                items_support_list.append({'Item': set(item) , 'Support': support})

        # Create dataframe
        df_frequent_sets = pd.DataFrame(items_support_list)
        return df_frequent_sets