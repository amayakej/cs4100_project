#import numpy as np 
import numpy as np
from scipy.signal import convolve2d

class State:
    # we are representing a 6 X 7 connect four board
    ROWS = 6
    COLUMNS = 7
    PLAYER1 = 1
    PLAYER2 = 2
    EMPTY = 0
    
    def __init__(self, grid, playerTurn):
        self.grid = grid
        #True if it is player 1's turn, False if it is player 2's turn
        self.playerTurn = playerTurn

    def makeBlankBoard():
        """
        Creates a blank board State

        Returns:
        State:The blank board State

        """
        return State(tuple([tuple([State.EMPTY]*State.COLUMNS)]*State.ROWS), True)
    
    def generateSuccessor(self, action):
        """
        Generates the successor State of the current when the current player
        performs the given action

        Parameters:
            action: (int):The column where the current player wants to place a piece
        
        Returns:
            State:The resulting state

        """
        piece = State.PLAYER1 if self.playerTurn else State.PLAYER2

        #column outside bounds of board or the column is already full
        if action < 0 or action > len(self.grid[0]) or self.grid[0][action] > 0:
            raise ValueError(f"illegal action: {action}")
        emptySpot = 0
        for row in range(len(self.grid)):
            if self.grid[row][action] != State.EMPTY:
                emptySpot -= 1
                break
            else:
                emptySpot += 1
        emptySpot = min(emptySpot, len(self.grid) - 1)

        oldRow = self.grid[emptySpot]
        newRow = oldRow[:action] + (piece,) + oldRow[action+1:]
        newGrid = self.grid[:emptySpot] + (newRow,) + self.grid[emptySpot+1:]

        return State(newGrid, not self.playerTurn)

    # decides if this terminal state is a win for the specified player (1 or 2)
    def __isWinForPlayer__(self, player):
        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        board = np.array(self.grid)
        for kernel in detection_kernels:
            if (convolve2d(board == player, kernel, mode="valid") == 4).any():
                return True
        return False

    def isWin(self):
        """
        Returns True if this State is a win for max

        Returns:
            bool: Whether it is a win for max or not

        """
        return self.__isWinForPlayer__(State.PLAYER1)

    def isLoss(self):
        """
        Returns True if this State is a loss for max

        Returns:
            bool: Whether it is a loss for max or not
            
        """
        return self.__isWinForPlayer__(State.PLAYER2)
    
    def isDraw(self):
        """
        Returns True if this State is a draw, so there are no more valid actions

        Returns:
            bool: Whether it is a draw
            
        """

        #Check is either player has won
        if self.isWin() or self.isLoss:
            return True
        
        #Check if all columns are filled
        for row in self.grid:
            if row[0] == State.EMPTY:
                return False
        return True

    def isTerminal(self):
        """
        Checks if the current State is a terminal state

        Returns:
            bool:Whether it is a terminal state or not
        """
        return self.isWin() or self.isLoss() or self.isDraw()

    # gets the utility of a terminal state
    def getUtility(self):
        if self.isWin:
            return 1
        if self.isLoss:
            return -1
        #Assume it is a terminal state, so return 0 for the draw
        else:
            return 0

    def __str__(self):
        ret = ""
        numSpaceX = 2
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

    def __eq__(self, other):
        if isinstance(other, State):
            return self.grid == other.grid
        return NotImplemented

    def __hash__(self):
        return hash(self.grid)
                  
# An Action is described by a target column
# to which the player drops his piece
class Action:

    def _init_(self, col):
        self.col = col

if __name__ == '__main__':
    #Horizontal win for player 1
    winningBoard = State.makeBlankBoard().generateSuccessor(0).generateSuccessor(0)
    winningBoard = winningBoard.generateSuccessor(1).generateSuccessor(1)
    winningBoard = winningBoard.generateSuccessor(2).generateSuccessor(2)
    print(winningBoard.isWin())
    winningBoard = winningBoard.generateSuccessor(3)

    print(winningBoard)
    print(winningBoard.isWin())
    print(winningBoard.isLoss())

    print("===========")

    #diagonal win for player1
    diagonalBoard = State.makeBlankBoard().generateSuccessor(0).generateSuccessor(1)
    diagonalBoard = diagonalBoard.generateSuccessor(1).generateSuccessor(2).generateSuccessor(2)
    diagonalBoard = diagonalBoard.generateSuccessor(3).generateSuccessor(2).generateSuccessor(3)
    diagonalBoard = diagonalBoard.generateSuccessor(3).generateSuccessor(5)

    print(diagonalBoard)
    print(diagonalBoard.isWin())
    
    diagonalBoard = diagonalBoard.generateSuccessor(3)

    print(diagonalBoard)
    print(diagonalBoard.isWin())






