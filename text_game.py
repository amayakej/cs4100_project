from model import State
from agent import MinMaxAgent

HISTORY_FILENAME = "game_history.txt"
class TextGame:

    #Takes in the depth for the MinMaxAgent as a parameter
    def __init__(self, depth):
        self.state = State.makeBlankBoard()
        self.agent = MinMaxAgent(depth)


    def getPlayerMove(self):
        """
        Gets the command line player's move and returns it. Continues trying until the player
        supplies a valid move.
        """
        validMove = False
        playerMove = -1
        legalMoves = self.state.getLegalActions()
        while not validMove:
            playerMove = input("\nEnter your move (0-6): ")
            validMove = playerMove.isdigit() and int(playerMove) in legalMoves
            if not validMove:
                print(f"Illegal Move: {playerMove}")
        return int(playerMove)

            

    def playGame(self):
        """
        Runs a command line version of Connect 4. The AI moves first and is player 1. The player on the
        command line is player 2.
        """
        #Store a history for each player
        playerHistory = []
        aiHistory = []
        playerMove = -1
        aiMove = -1
        validMove = False
        while not self.state.isTerminal():
            print(self.state, "\n")

            aiMove = self.agent.getMove(self.state)
            self.state = self.state.generateSuccessor(aiMove)
            aiHistory.append(aiMove)

            print(f"AI Move: {aiMove}")
            print(self.state)

            if self.state.isTerminal():
                break

            playerMove = self.getPlayerMove()
            self.state = self.state.generateSuccessor(playerMove)
            playerHistory.append(playerMove)

            print(f"Your Move: {playerMove}\n")
            print(self.state)
            print("=============================================\n")

        winner = None
        if self.state.isWin():
            winner = State.PLAYER1
        elif self.state.isLoss():
            winner = State.PLAYER2
        
        win_msg = ""
        if winner is None:
            win_msg = "\nIts a draw!"
        else:
            win_msg = f"\nPlayer {winner} wins!"
        print(win_msg)
        self.state = State.makeBlankBoard()
        return aiHistory, playerHistory, winner

if __name__ == '__main__':
    game = TextGame(5)

    aiHistory, playerHistory, winner = game.playGame()

    #Write the history of moves for each player to a file
    with open(HISTORY_FILENAME, "a") as f:
        f.write("AI History:\n")
        f.write(" ".join(str([move for move in aiHistory])))
        f.write("\n Player History:\n")
        f.write(" ".join(str([move for move in playerHistory])))
        if winner is not None:
            f.write(f"\n Player {winner} wins!")
        else:
            f.write(f"\nIts a draw.")
        f.write("\n=================================================\n")