import pandas as pd
from tqdm import tqdm
import multiprocessing as mp
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

    def __init__(self, baskets, min_support, n, parallel=True):
        self.baskets = baskets
        self.min_support = min_support
        self.n = n
        self.parallel = parallel

    def count_candidates(self, candidate, frequent_items, s):
        """
        Count the occurrences of candidates in a list of baskets.
        """
        set_list = []
        for i in candidate:
            set_list.append(set(frequent_items[i]))
        intersection = set.intersection(*set_list)
        if len(intersection) >= s:
            return {candidate: intersection}
        return {}

    def generate_candidates(self, frequent_sets, k):
        """
        Generates only candidates whose all subsets have sufficient support.
        This approache ensures that we are only generating and checking the 
        candidates that have a chance of being frequent, which is the main idea 
        behind pruning in the Apriori algorithm.

        @param frequent_sets: Dictionary of frequent sets, e.g. {key = item: value = itemsets_id_with_item}
        @param k: Size of the itemsets to generate
        """
        prev = list(frequent_sets.keys())
        if k == 2:
            prev = [set([item]) for item in prev]

        candidates = {}
        for itemset1 in prev:
            for itemset2 in prev:
                if itemset1 != itemset2:
                    candidate = set(itemset1).union(itemset2) 
                    if len(candidate) == k: # If the number of items in the candidate is equal to k
                        candidates[tuple(candidate)] = 0
            
        tuples_list = list(candidates.keys())
        
        return tuples_list

    def apriori(self, baskets, min_support):
        """
        A-Priori algorithm for finding frequent itemsets.
        """
        s = min_support * self.n 

        frequent_items = dict()
        for key in baskets.keys():
            if len(baskets[key]) >= s:
                frequent_items[key] = baskets[key]

        frequent_sets = frequent_items
        output = frequent_items
        # TODO: Prune here?

        k = 2   # Size of itemsets
        # Generate candidates for the first iteration
        #candidates = list(combinations(frequent_items.keys(), k))
        candidates = self.generate_candidates(frequent_sets, k)

        # Create a TQDM progress bar
        progress_bar = tqdm(total=len(candidates), desc='Candidates', leave=False)
        while candidates:
            # Count occurrences of candidates in buckets
            if self.parallel:
                pool = mp.Pool(mp.cpu_count())
                result = pool.starmap(self.count_candidates, [(candidate, frequent_items, s) for candidate in candidates])
                pool.close()
            else:
                result = []
                for candidate in candidates:
                    result.append(self.count_candidates(candidate, frequent_items, s))

            frequent_sets = {candidate: support for candidate_support in result for candidate, support in candidate_support.items()}
            output.update(frequent_sets)
            # Generate candidates for the next iteration
            k += 1
            candidates = self.generate_candidates(frequent_sets, k)
            progress_bar.update()   # Update progress bar
            progress_bar.refresh()  # Refresh progress bar

            
        return output
    
    def __call__(self):
        frequent_sets = self.apriori(self.baskets, min_support=self.min_support)

        df_frequent_sets = pd.DataFrame(columns=['Itemset', 'Support'])
        for key, value in frequent_sets.items():
            df_temp = pd.DataFrame({'Itemset': [key], 'Support': [len(value)]})
            df_frequent_sets = pd.concat([df_frequent_sets, df_temp], axis=0, ignore_index=True)

        return df_frequent_sets, frequent_sets
    
class AssociationRule():

    def __init__(self, frequent_sets, min_confidence, n):
        self.frequent_sets = frequent_sets   # Dictionary of frequent sets, e.g. {key = itemset: value = basket_id_containing_itemset}
        self.min_confidence = min_confidence
        self.n = n

    def generate_rules(self):
        """
        Generate association rules from frequent itemsets.
        • Confidence (A --> B) = Support(A and B) / Support(A)
        • Interest = P(A and B) - P(A)P(B) = Confidence(A --> B) - P(B)
        """
        rules = []

        for itemset in self.frequent_sets.keys():
            itemset_support = len(self.frequent_sets[itemset])   # Support of the itemset
            if type(itemset) == int:
                itemset = {itemset}
            else:
                itemset = set(itemset)

            # Generate all possible combinations of items in the frequent itemset
            for j in range(1, len(itemset)):
                for antecedent in combinations(itemset, j):
                    antecedent = set(antecedent)      # Antecedent is a set of items
                    consequent = itemset - antecedent # Consequent is the rest of the items in the itemset

                    # Find the support of the antecedent and consequent
                    look_up_key_a = tuple(antecedent) if len(antecedent) > 1 else antecedent.pop() # Get index/key of the antecedent
                    look_up_key_c = tuple(consequent) if len(consequent) > 1 else consequent.pop()
                    support_antecedent = len(self.frequent_sets[look_up_key_a])
                    support_consequent = len(self.frequent_sets[look_up_key_c])
                    
                    # Calculate confidence
                    confidence = itemset_support / support_antecedent
                    # Confidence({1, 4}--->{2}) = Support({1,4})/Support({1,2,4}) = 2/2 = 1.0

                    # Calculate interest
                    interest = confidence - (support_consequent/self.n)
                    # Interest({1, 4}--->{2}): 1.0 - (6/7) = 0.1428571428571429 

                    if confidence >= self.min_confidence:
                        rules.append({'A': look_up_key_a, 'B': look_up_key_c, 'Confidence': round(confidence,3), 'Interest': round(interest,3)})

        return pd.DataFrame(rules)

    def __call__(self):
        rules = self.generate_rules()
        return rules