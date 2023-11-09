def compare_signatures(signature1, signature2):
    '''
    Compares two minHash signatures and calculates the similarity
    @param signature1: minHash signature
    @param signature2: minHash signature
    @return similarity: similarity between two minHash signatures
    '''
    count = 0
    for i in range(len(signature1)):
        if signature1[i] == signature2[i]:
            count += 1
    similarity = count / len(signature1)
    return similarity