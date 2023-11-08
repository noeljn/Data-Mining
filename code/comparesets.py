
class CompareSet:
    def __init__(self, set1, set2):
        self.set1 = set1
        self.set2 = set2

    def jaccard_similarity(self):
        intersection = len(self.set1.intersection(self.set2))
        union = len(self.set1.union(self.set2))
        return intersection / union


