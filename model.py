#import numpy as np 

class State:
    # we are representing a 6 X 7 connect four board
    ROWS = 6
    COLUMNS = 7
    
    def __init__(self, grid, playerTurn):
        self.grid = grid
        #True if it is player 1's turn, False if it is player 2's turn
        self.playerTurn = playerTurn

    def makeBlankBoard():
        return State(tuple([tuple([0]*State.COLUMNS)]*State.ROWS), True)
    
    def generateSuccessor(self, action):
        #column outside bounds of board or the column is already full
        if action < 0 or action > len(self.grid[0]) or self.grid[0][action] > 0:
            raise ValueError(f"illegal action: {action}")
        emptySpot = 0
        for row in range(len(self.grid)):
            if self.grid[row][action] > 0:
                emptySpot -= 1
                break
            else:
                emptySpot += 1
        emptySpot = min(emptySpot, len(self.grid) - 1)
        newRow = list(self.grid[emptySpot])
        newRow[action] = 1 if self.playerTurn else 2
        newGrid = self.grid[:emptySpot] + (tuple(newRow),) + self.grid[emptySpot+1:]

        return State(newGrid, not self.playerTurn)

    
    # decides if the current state is a terminal state
    def isTerminal(self):
        pass

    # decides if this terminal state is a win for max
    def isWin(self):
        pass

    # decides if this terminal state is a loss for max
    def isLoss(self):
        pass
    
    # decides if this terminal state is a draw
    def isDraw(self):
        pass

    # gets the utility of the the terminal state
    def getUtility(self):
        if self.isTerminal and self.isDraw:
            return 0
        if self.isTerminal and self.isWin:
            return 1
        if self.isTerminal and self.isLoss:
            return -1

    def __str__(self):
        ret = ""
        numSpaceX = 3
        numSpaceY = 1
        for row in range(len(self.grid)):
            cur_row = ""
            for col in range(len(self.grid[0])):
                cur_row += str(self.grid[row][col])
                if col < len(self.grid[0]) - 1:
                    cur_row += " "*numSpaceX
            ret += cur_row
            if row < len(self.grid) - 1:
                ret += "\n"*numSpaceY
        return ret
            
        
# An Action is described by a target column
# to which the player drops his piece
class Action:

    def _init_(self, col):
        self.col = col



if __name__ == '__main__':
    #both players place in column 1
    print(State.makeBlankBoard().generateSuccessor(1).generateSuccessor(1).generateSuccessor(1).generateSuccessor(1))




