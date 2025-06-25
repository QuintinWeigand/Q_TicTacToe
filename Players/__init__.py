class Player:
    def __init__(self, playerNumber):
        self.__playerNumber = playerNumber
        self.__winner = False
        self.__moves = []

    def addMove(self, movePos):
        self.__moves.append(movePos)

    def getMoves(self) -> list:
        return [list(move) for move in self.__moves]

    def setPlayerWinner(self):
        self.__winner = True

    def getPlayerStatus(self) -> bool:
        return self.__winner
    
    # TODO: Update for new database entry
    def dictify(self) -> dict:
        return {
                    "Player Number": self.__playerNumber,
                    "isWinner": self.__winner,
                    "moves": self.getMoves()
               }