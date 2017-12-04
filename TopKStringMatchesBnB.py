import pygtrie
import collections
from TopKStringMatchesCommon import TopKStringMatchesCommon

class TopKStringMatchesBnB(TopKStringMatchesCommon):

    def __init__(self, filePath, q, k):
        TopKStringMatchesCommon.__init__(self, filePath, q, k)
        self.getQGramDictionary()

    def getQGramDictionary(self):
        self.populateWordList()
        for index, str_val in self.str_collection.items():
            ngram_list = self.chunks(str_val)
            for ngram in ngram_list:
                if self.trie.has_key(ngram):
                    self.trie[ngram][len(str_val)].append(index)
                else:
                    self.trie[ngram] = collections.defaultdict(lambda: [])
                    self.trie[ngram][len(str_val)].append(index)

    def getTopKMatches(self, query, k):
        self.kSize = k
        self.inverted_list_scanned = 0
        cl = list(self.chunks(query))
        ttopk = 1
        ld = 0

        topKMatches = []
        while True:
            topKMatchesIterVariant = []
            frequency = collections.defaultdict(int)
            candidates = []
            sl = []
            for query_ngram in cl:
                if (len(query) - ld > 0):
                    sl += self.trie[query_ngram][len(query) - ld]
                sl += self.trie[query_ngram][len(query) + ld]
            sl = list(set(sl))

            for str_id in sl:
                string_val = self.str_collection[str_id]
                for query_ngram in cl:
                    if query_ngram in string_val:
                        frequency[str_id] += 1
                        if (frequency[str_id] == ttopk):
                            candidates.append(str_id)

            self.inverted_list_scanned += len(candidates)
            for candidate in candidates:
                ed = self.minimumEditDistance(self.str_collection[candidate], query)
                topKMatchesIterVariant.append((candidate, ed))
                topKMatches.append((candidate, ed))

            topKMatchesIterVariant = sorted(topKMatchesIterVariant, key=lambda x: x[1])[:self.kSize]
            topKMatches = sorted(topKMatches, key=lambda x: x[1])[:self.kSize]

            if (len(topKMatches) >= self.kSize):
                if(topKMatches[self.kSize-1][1] <= ld+1):
                    break
                ttopk = max(ttopk, self.similiarityScore(query, self.str_collection[topKMatches[self.kSize-1][0]], topKMatches[self.kSize-1][1]))

            ld += 1
            if (len(query) + ld > self.maxLength):
                break

        return [(self.str_collection[key], val) for key, val in topKMatches]