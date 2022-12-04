from model import State


#Abstract class for game playing agents
class GameAgent():
    def getMove(state: State):
        raise NotImplementedError()


class MinMaxAgent(GameAgent):

    def __init__(self, depth):
        self.depth = depth

    def getMove(self, state: State):
        return self.get_value(state, self.depth,  float('-inf'), float('inf'))[1]

    def max_value(self, state, depth, alpha, beta):
        val = float('-inf')

        legal_actions = state.getLegalActions()
        max_action = legal_actions[0]
        new_alpha = alpha
        for action in legal_actions:
            successor = state.generateSuccessor(action)
            next_val = self.get_value(successor, depth - 1, new_alpha, beta)[0]
            if next_val > val:
                val = next_val
                max_action = action
            if val > beta:
                return val, max_action
            new_alpha = max(new_alpha, val)
            
        return val, max_action
    

    def min_value(self, state, depth, alpha, beta):
        val = float('inf')

        legal_actions = state.getLegalActions()
        min_action = legal_actions[0]
        new_beta = beta
        for action in legal_actions:
            successor = state.generateSuccessor(action)
            next_val = self.get_value(successor, depth - 1, alpha, new_beta)[0]
            if next_val < val:
                val = next_val
                min_action = action
            if val < alpha:
                return val, min_action
            new_beta = min(new_beta, val)
            
        return val, min_action

    def get_value(self, state, depth, alpha, beta):
        
        #next_agent = (agent + 1) % state.getNumAgents()
        if depth == 0 or len(state.getLegalActions()) == 0:
            #This is where to bring in the machine learning aspect
            return self.evaluationFunction(state), []

        elif state.playerTurn:
            return self.max_value(state, depth, alpha, beta)
        else:
            return self.min_value(state, depth, alpha, beta)

    def evaluationFunction(self, state):
        return state.getUtility()
        
if __name__ == '__main__':
    agent = MinMaxAgent(3)
    diagonalBoard = State.makeBlankBoard().generateSuccessor(0).generateSuccessor(1)
    diagonalBoard = diagonalBoard.generateSuccessor(1).generateSuccessor(2).generateSuccessor(2)
    diagonalBoard = diagonalBoard.generateSuccessor(3).generateSuccessor(2).generateSuccessor(3)
    diagonalBoard = diagonalBoard.generateSuccessor(3).generateSuccessor(5)
    print(diagonalBoard)
    print(agent.getMove(diagonalBoard))