import time
from TopKStringMatchesNaive import TopKStringMatchesNaive
from TopKStringMatchesBnB import TopKStringMatchesBnB

class AlgoAnalyzer():
    def __init__(self, dictPath):
        self.naive_matcher = TopKStringMatchesNaive(dictPath, 2, 2)
        self.bnb_matcher = TopKStringMatchesBnB(dictPath, 2, 2)

    def compare_results(self, k, print_res=True):
        start = time.time()
        topKMatches = self.naive_matcher.getTopKMatches("blunt", k)
        end = time.time()
        print("Time taken to get Top-{} String Matches using Naive Method - {} seconds".format(k, str(end - start)))
        print("Size of Inverted lists scanned during the Naive process - ", str(self.naive_matcher.inverted_list_scanned))
        if print_res:
            self.print_result(topKMatches)

        start = time.time()
        topKMatches = self.bnb_matcher.getTopKMatches("blunt", k)
        end = time.time()
        print("Time taken to get Top-{} String Matches using Branch And Bound Method - {} seconds".format(k, str(end - start)))
        print("Size of Inverted lists scanned during the Branch and Bound process - ", str(self.bnb_matcher.inverted_list_scanned))
        if print_res:
            self.print_result(topKMatches)

        print("\n")

    def print_result(self, topKMatches):
        print("string\t\tsimilarity score")
        for tup in topKMatches:
            print('{:10s}'.format(tup[0]) + "\t\t" + str(tup[1]))

        print("\n\n")

if __name__ == '__main__':
    dictPath = "./dict.txt"
    analyzer = AlgoAnalyzer(dictPath)
    analyzer.compare_results(10, True)
    analyzer.compare_results(100, False)
    analyzer.compare_results(500, False)
    analyzer.compare_results(1000, False)
    analyzer.compare_results(1500, False)
