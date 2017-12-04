import pygtrie
import collections
from TopKStringMatchesCommon import TopKStringMatchesCommon

class TopKStringMatchesNaive(TopKStringMatchesCommon):

    def __init__(self, filePath, q, k):
        TopKStringMatchesCommon.__init__(self, filePath, q, k)
        self.getQGramDictionary()

    def getQGramDictionary(self):
        self.populateWordList()
        for index, str_val in self.str_collection.items():
            ngram_list = self.chunks(str_val)
            for ngram in ngram_list:
                if self.trie.has_key(ngram):
                    self.trie[ngram].append(index)
                else:
                    self.trie[ngram] = [index]

    def getTopKMatches(self, query, k):
        self.kSize = k
        self.inverted_list_scanned = 0
        cl = list(self.chunks(query))
        ngram_match_count = collections.defaultdict(lambda: [0,100])
        for query_ngram in cl:
            if not self.trie.has_key(query_ngram):
                continue

            #key is present in dict
            sl = self.trie[query_ngram]
            for str_id in sl:
                ngram_match_count[str_id][0] += 1

        self.inverted_list_scanned = len(ngram_match_count.keys())
        for key, val in ngram_match_count.items():
            val[1] = self.minimumEditDistance(query, self.str_collection[key])

        return [(self.str_collection[key], str(val[1]))for key, val in sorted(ngram_match_count.items(), key=lambda t: t[1][1])[:self.kSize]]