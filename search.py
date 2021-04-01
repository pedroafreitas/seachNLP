import heapq, collections, re, sys, time, os, random

############################################################
# Abstrai os problemas de busca dos algoritmos de busca

class SearchProblem:
    # Retorna o Estado inicial.
    def startState(self): raise NotImplementedError("Override me")

    # Retorna se o Estado é Final
    def isEnd(self, state): raise NotImplementedError("Override me")

    # Retorna a lista com as tuplas (action, newState, cost) correspondentes aos nós da fronteira
    def succAndCost(self, state): raise NotImplementedError("Override me")


############################################################
# Busca Uniforme

class UniformCostSearch():
    def __init__(self, verbose=0):
        self.verbose = verbose

    def solve(self, problem):
        # Se o caminho existe, configura |actions| e |totalCost|.
        # Se não, define como None
        self.actions = None
        self.totalCost = None
        self.numStatesExplored = 0

        # Inicializa as estruturas
        frontier = PriorityQueue()  # Explora os dados na fronteira
        pointers = {}  # mapeia o estado para (action, previous state)

        # Add o estado inicial
        startState = problem.startState()
        frontier.update(startState, 0)

        while True:
            # Remove o estado da fila com o menor pastCost (priority).
            state, pastCost = frontier.removeMin()
            if state == None: break
            self.numStatesExplored += 1
            if self.verbose >= 2:
                print(("Explorando %s com pastCost %s" % (state, pastCost)))

            # Checa se chegamos ao estado final e extrai a solucão
            if problem.isEnd(state):
                self.actions = []
                while state != startState:
                    action, prevState = pointers[state]
                    self.actions.append(action)
                    state = prevState
                self.actions.reverse()
                self.totalCost = pastCost
                if self.verbose >= 1:
                    print(("numEstadosExplorados = %d" % self.numStatesExplored))
                    print(("custoTotal = %s" % self.totalCost))
                    print(("acões = %s" % self.actions))
                return

            # Expande do |state| para o novo sucessor de estados, atualizando a fronteira para cada novo estado
            for action, newState, cost in problem.succAndCost(state):
                if self.verbose >= 3:
                    print(("  Acão %s => %s com custo %s + %s" % (action, newState, pastCost, cost)))
                if frontier.update(newState, pastCost + cost):
                    # Found better way to go to |newState|, update pointer.
                    pointers[newState] = (action, state)
        if self.verbose >= 1:
            print("Nao encontrou o caminho")

# Criando a fila para a busca
class PriorityQueue:
    def  __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}  # estado para prioridade

    # Insere |state| na pilha com prioridade |newPriority| se
    # |state| não está na pilha ou se |newPriority| é menor que a prioridade existente
    # Retorna caso a fila de prioridade foi atualizada
    def update(self, state, newPriority):
        oldPriority = self.priorities.get(state)
        if oldPriority == None or newPriority < oldPriority:
            self.priorities[state] = newPriority
            heapq.heappush(self.heap, (newPriority, state))
            return True
        return False

    # Retorna (state com menor prioridade, prioridade)
    # ou (None, None) se a fila de prioridade está vazia
    def removeMin(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE: continue  
            self.priorities[state] = self.DONE
            return (state, priority)
        return (None, None) # Quando não sobra nada
