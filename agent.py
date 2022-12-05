from model import State
import numpy as np
from scipy.signal import convolve2d

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
        #print(legal_actions)
        max_action = legal_actions[0]
        new_alpha = alpha
        for action in legal_actions:
            successor = state.generateSuccessor(action)
            if State.isTerminal == 'False':
                next_val = self.get_value(successor, depth - 1, new_alpha, beta)[0]
            else: 
                next_val = self.getUtility(successor)
            if next_val > val:
                val = next_val
                print(action)
                max_action = action
            if val > beta:           
                return val, max_action           
            new_alpha = max(new_alpha, val)                
        return val, max_action
    

    def min_value(self, state, depth, alpha, beta):
        val = float('inf')

        legal_actions = state.getLegalActions()
        #print(legal_actions)
        min_action = legal_actions[0]
        new_beta = beta
        for action in legal_actions:
            successor = state.generateSuccessor(action)
            if State.isTerminal == 'False':
                next_val = self.get_value(successor, depth - 1, alpha, new_beta)[0]
            else: 
                next_val = self.getUtility(successor)            
            if next_val < val:
                val = next_val
                print(action)
                min_action = action
            if val < alpha:
                return val, min_action
            new_beta = min(new_beta, val)
            
        return val, min_action

    def get_value(self, state, depth, alpha, beta):
        
        #next_agent = (agent + 1) % state.getNumAgents()
        if depth == 0 or len(state.getLegalActions()) == 0:
            #This is where to bring in the machine learning aspect
            return self.evaluation_function(state), -1

        elif state.playerTurn:
            return self.max_value(state, depth, alpha, beta)
        else:
            return self.min_value(state, depth, alpha, beta)

    # gets the utility of a terminal state
    def getUtility(self, state):
        if state.isWin(): 
            return 10000000
        if state.isLoss():
            return -5000
        #Assume it is a terminal state, so return 0 for the draw
        else:
            return self.evaluation_function(state)       
        
    def checkForStreak(self, state, player, num):
        counter = 0 
        horizontal_kernel = np.array([[1] * num]) 
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(num, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        board = np.array(state.grid)
        for kernel in detection_kernels:
            counter += np.sum(convolve2d(board == player, kernel, mode="valid") == num)
        return counter        

    def evaluation_function(self, state):
        my_threes = self.checkForStreak(state, State.PLAYER1, 3)
        my_twos = self.checkForStreak(state, State.PLAYER1, 2)
        comp_threes = self.checkForStreak(state, State.PLAYER2, 3)
        comp_twos = self.checkForStreak(state, State.PLAYER2, 2)
        return (my_threes * 5 + my_twos * 2) - (comp_threes * 5 + comp_twos * 2)
        
if __name__ == '__main__':
    agent = MinMaxAgent(2)
    diagonalBoard = State.makeBlankBoard().generateSuccessor(0).generateSuccessor(1)
    diagonalBoard = diagonalBoard.generateSuccessor(1).generateSuccessor(2).generateSuccessor(2)
    diagonalBoard = diagonalBoard.generateSuccessor(3).generateSuccessor(2).generateSuccessor(3)
    diagonalBoard = diagonalBoard.generateSuccessor(3).generateSuccessor(5)
    test = State.makeBlankBoard().generateSuccessor(0).generateSuccessor(5).generateSuccessor(1)
    print(test)
    print(agent.checkForStreak(test, 1, 3))
    test = test.generateSuccessor(5).generateSuccessor(2)
    print(agent.checkForStreak(test, 1, 3))
    test = test.generateSuccessor(6).generateSuccessor(0).generateSuccessor(5).generateSuccessor(0)
    print(agent.checkForStreak(test, 1, 3))

    print(diagonalBoard)
    print(diagonalBoard.playerTurn)
    print(agent.getMove(diagonalBoard))
    


    
    