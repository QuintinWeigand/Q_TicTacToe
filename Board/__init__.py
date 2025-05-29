class Board:
    def __init__(self):
        self.__gameboard = [['1','2','3'],['4','5','6'],['7','8','9']]

    def displayBoard(self):
        # print("In displayBoard()")
        for row in range(len(self.__gameboard)):
            for col in range(len(self.__gameboard[0])):
                print(self.__gameboard[row][col] + " ", end="")
            print()

    def get(self, row, col) -> chr:
        returnCharacter = None
        if self.__validIndex(row, col):
            returnCharacter = self.__gameboard[row][col]
        else:
            print("You did not enter a valid index!!!")
        
        return returnCharacter
    
    def set(self, row, col, c: chr) -> bool:
        hasBeenSet = False
        if self.__validIndex(row, col):
            if self.__gameboard[row][col].isdigit():
                self.__gameboard[row][col] = c
                hasBeenSet = True
            else:
                print("Position Taken!")
        else:
            print("Position Invalid!")

        return hasBeenSet

    def hasWinner(self) -> bool:
        # Check rows
        for row in self.__gameboard:
            if len(set(row)) == 1:
                return True

        # Check columns
        for col in range(len(self.__gameboard[0])):
            column = [self.__gameboard[row][col] for row in range(len(self.__gameboard))]
            if len(set(column)) == 1:
                return True

        # Check diagonals
        diag1 = [self.__gameboard[i][i] for i in range(len(self.__gameboard))]
        if len(set(diag1)) == 1:
            return True

        diag2 = [self.__gameboard[i][len(self.__gameboard)-1-i] for i in range(len(self.__gameboard))]
        if len(set(diag2)) == 1:
            return True

        return False

    def __validIndex(self, row, col) -> bool:
        # print("In validIndex!")
        isValidIndex = False
        if row < len(self.__gameboard) and row >= 0:
            if col < len(self.__gameboard[0]) and col >= 0:
                isValidIndex = True

        return isValidIndex
    
    @staticmethod
    def convertNumPositionToIndex(numPos: int):
        
        if 1 <= numPos <= 9:
            row = (numPos - 1) // 3
            col = (numPos - 1) % 3
            return row, col
        else:
            raise ValueError("Position must be between 1 and 9")

