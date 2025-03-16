from w2v_algo import Algo

class HebrewSimilarWords:
    def __init__(self):
        self.algo = Algo('wiki-w2v')
        self._num_results = 10

    def set_num_results(self, num_results):
        self._num_results = num_results

    def get_most_similar(self, word):
        algos_similarity_results = self.algo.search_similar(word, self._num_results + 1)
        return algos_similarity_results[word][1:] # skip the first one, since it is guaranteed to be the word itself...
    
    def calc_similarity(self, word1, word2):
        return (word1, word2, self.algo.calc_similarity(word1, word2))