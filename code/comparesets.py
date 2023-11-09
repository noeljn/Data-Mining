def jaccard_similarity(hashed_shingles_set_1, hashed_shingles_set_2):
        '''
        Calculates the Jaccard similarity between two sets of singles
        @param hashed_shingles_set_1: a set of shingles (is included in a Shingling-object)
        @param hashed_shingles_set_2: a set of shingles (is included in a Shingling-object)
        @return computed Jaccard similarity
        '''

        intersection = len(hashed_shingles_set_1.intersection(hashed_shingles_set_2))
        union = len(hashed_shingles_set_1.union(hashed_shingles_set_2))
        return intersection / union