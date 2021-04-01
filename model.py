import shell
import search
import util

############################################################
# Problema 1: Problema de Segmentacao usando unigrama

class SegmentationProblem(search.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        return self.query
        

    def isEnd(self, state):
        return len(state) == 0
        
    def succAndCost(self, state):
        result = []
        if not self.isEnd(state):
            for i in range (len(state),0,-1):
                action = state[:i]
                cost = self.unigramCost(action)
                remainingText = state[len(action):]
                result.append((action,remainingText,cost))
        return result
        
def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = search.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    words=' '.join(ucs.actions)
    return words
    
############################################################
# Problema 2: Problema de insercao de vogal usando bigrama

class VowelInsertionProblem(search.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        return (self.queryWords[0],0)
        
    def isEnd(self, state):
        return state[1]==len(self.queryWords)-1
            
    def succAndCost(self, state):
        result = []
        index=state[1]+1
        choices = self.possibleFills(self.queryWords[index]).copy()
        if len(choices)==0:
            choices.add(self.queryWords[index])
        for action in choices:
            cost=self.bigramCost(state[0],action)
            result.append((action, (action,index), cost))
        return result
        
def insertVowels(queryWords, bigramCost, possibleFills):
    if len(queryWords)==0:
        return ''
    else:
        queryWords.insert(0,util.SENTENCE_BEGIN)
    ucs = search.UniformCostSearch(verbose=1)
    ucs.solve(VowelInsertionProblem(queryWords,bigramCost,possibleFills))
    words = ' '.join(ucs.actions)
    return words

if __name__ == '__main__':
    
    shell.main()
