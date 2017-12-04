import pygtrie
import collections

class TopKStringMatchesCommon:
    trie = None
    str_collection = None
    str_list = []
    qSize = 0
    kSize = 1
    maxLength = 0
    inverted_list_scanned = 0

    def __init__(self, filePath, q, k):
        self.str_collection = collections.defaultdict(None)
        self.trie = pygtrie.StringTrie()
        self.qSize = q
        self.kSize = k
        self.dictionaryFile = filePath

    def chunks(self, l, step=1):
        """ Yield successive n-sized chunks from l with a given step
        """
        n = self.qSize
        for i in range(0, len(l)-n+1, step):
            yield l[i:i+n]

    def minimumEditDistance(self, s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        distances = range(len(s1) + 1)
        for index2, char2 in enumerate(s2):
            newDistances = [index2 + 1]
            for index1, char1 in enumerate(s1):
                if char1 == char2:
                    newDistances.append(distances[index1])
                else:
                    newDistances.append(1 + min((distances[index1],
                                                 distances[index1 + 1],
                                                 newDistances[-1])))
            distances = newDistances
        return distances[-1]

    def populateWordList(self):
        with open(self.dictionaryFile) as f:
            content = f.readlines()

        str_list = [x.strip() for x in content]
        for index, str_val in enumerate(str_list):
            if (len(str_val) > self.maxLength):
                self.maxLength = len(str_val)
            self.str_collection[index] = str_val


    def similiarityScore(self, query, match, ed):
        return max(len(query), len(match)) - self.qSize + 1 - (self.qSize * ed)