import numpy as np
from numpy import linalg as LA
import itertools
from os.path import join

class Algo:
    def __init__(self, data_path):
        self._data_path = data_path
        self._load_algo_data()

    def _load_algo_data(self):
        path = self._data_path
        # Load words list as before
        with open(join(path, "words_list.txt"), 'r', encoding='utf-8') as f:
            cur_words = f.readlines()
        cur_words = [word[:-1] for word in cur_words]  # Remove newline
        
        # Lazily load vectors using memory mapping
        self._words_list = cur_words
        self._vecs = np.load(join(path, "words_vectors.npy"), mmap_mode='r')  # Use mmap_mode='r' for lazy loading
        
        # Normalize vectors (this still requires the vectors to be in memory for normalization)
        self._vecs = self._vecs / LA.norm(self._vecs, axis=1).reshape((len(self._vecs), 1))
        
    def calc_similarity(self, word1, word2):
        index1 = self._words_list.index(as_appears_in_algo(word1))
        index2 = self._words_list.index(as_appears_in_algo(word2))
        
        # Fetch vectors lazily from memory-mapped file
        vec1 = self._vecs[index1]
        vec2 = self._vecs[index2]
        
        return sum([vec1[i] * vec2[i] for i in range(len(vec1))])

    def search_similar(self, word, num_results):
        results_dict = {}
        wanted_ind = []
        try:
            wanted_ind.append(self._words_list.index(as_appears_in_algo(word)))
        except:
            if len(wanted_ind) == 0:
                return {}
        
        for word_ind in wanted_ind:
            results = self._top_similar_smart(self._vecs[word_ind], num_results=num_results)
            results_dict[self._words_list[word_ind]] = results
        return results_dict

    def search_analogy(self, input_words, num_results):
        results_tuples = []
        words_idx = []
        for in_word in input_words:
            cur_word_idx = []
            try:
                cur_word_idx.append(self._words_list.index(as_appears_in_algo(in_word)))
            except:
                if len(cur_word_idx) == 0:
                    return {}
            words_idx.append(cur_word_idx)

        for input_pos_idx_option in list(itertools.product(*words_idx)):
            # Use memory-mapped vectors for analogy calculation
            wanted_vec = self._vecs[input_pos_idx_option[2]] - self._vecs[input_pos_idx_option[0]] + \
                         self._vecs[input_pos_idx_option[1]]
            results = self._top_similar_smart(wanted_vec, num_results=num_results)
            results_tuples.append(([self._words_list[word_ind] for word_ind in input_pos_idx_option], results))
        return results_tuples

    def _top_similar_smart(self, wanted_vec, num_results=10):
        idx, sims = self._top_similar(wanted_vec, num_results)
        results = [{'word': self._words_list[idx[i]], 'similarity': sims[i]} for i in range(num_results)]
        return results

    def _top_similar(self, vec, results_to_show=10):
        try:
            # Use memory-mapped vectors to calculate similarity
            mul = np.dot(self._vecs, vec)
        except:
            try:
                mul = np.dot(vec, self._vecs)
            except:
                for i in range(len(self._vecs)):
                    if self._vecs[i].shape[0] != 100 or self._vecs[i].shape[0] != 200:
                        print("Error at top similar for vector number {} with shape {}".format(i, self._vecs[i].shape))
        vec_norm = LA.norm(vec)
        sims = mul / vec_norm
        ind = np.argpartition(sims, -results_to_show)[-results_to_show:]
        ind = (ind[np.argsort(sims[ind])])[::-1]
        return ind, sims[ind]

def as_appears_in_algo(word):
    word = word.lstrip()
    word = word.replace("-", "~")
    word = word.replace(" ", "~")
    return word

def as_appear_in_site(word):
    word = word.replace("~", " ")
    return word