class Board:
    def __init__(self):
        self.__gameboard = [['1','2','3'],['4','5','6'],['7','8','9']]
        self.__gamestatus = {}

    def displayBoard(self):
        # print("In displayBoard()")
        for row in range(len(self.__gameboard)):
            for col in range(len(self.__gameboard[0])):
                print(self.__gameboard[row][col] + " ", end="")
            print()

    def getBoard(self) -> str:
        str_board = ""

        for row in range(len(self.__gameboard)):
            for col in range(len(self.__gameboard[0])):
                str_board += self.__gameboard[row][col]
            str_board += "\n"

        return str_board

    def get(self, row, col) -> chr:
        returnCharacter = None
        if self.__validIndex(row, col):
            returnCharacter = self.__gameboard[row][col]
        else:
            print("You did not enter a valid index!!!")
        
        return returnCharacter
    
    def getGameStatus(self) -> dict:
        return self.__gamestatus.copy()
    
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

    def hasWinnerOrDraw(self) -> bool:
        winner = None

        # Check rows
        for row in self.__gameboard:
            if len(set(row)) == 1 and not row[0].isdigit():
                winner = row[0]
                break

        # Check columns
        if not winner:
            for col in range(len(self.__gameboard[0])):
                column = [self.__gameboard[row][col] for row in range(len(self.__gameboard))]
                if len(set(column)) == 1 and not column[0].isdigit():
                    winner = column[0]
                    break

        # Check diagonals
        if not winner:
            diag1 = [self.__gameboard[i][i] for i in range(len(self.__gameboard))]
            if len(set(diag1)) == 1 and not diag1[0].isdigit():
                winner = diag1[0]

        if not winner:
            diag2 = [self.__gameboard[i][len(self.__gameboard)-1-i] for i in range(len(self.__gameboard))]
            if len(set(diag2)) == 1 and not diag2[0].isdigit():
                winner = diag2[0]

        if winner:
            if winner == 'X':
                self.__gamestatus["winner"] = "Player1"
            elif winner == 'O':
                self.__gamestatus["winner"] = "Player2"
            return True

        # Check for draw: if no digits left, it's a draw
        for row in self.__gameboard:
            for cell in row:
                if cell.isdigit():
                    return False  # Still moves left

        # No winner and no moves left: draw
        self.__gamestatus["winner"] = "Draw"
        return True

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

