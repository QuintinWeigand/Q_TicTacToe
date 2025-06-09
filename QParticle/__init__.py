class QParticle:
    def __init__(self, subscript: int, creation_number: int):
        self.__subscript = subscript
        self.__creation_number = creation_number

    # Creating our equal operator
    def __eq__(self, other) -> bool:
        if isinstance(other, QParticle):
            return self.__subscript == other.__subscript
        return False
    
    def __str__(self):
        return f"{self.__subscript}+{self.__creation_number}"

    def get_subscript(self) -> int:
        return self.__subscript
    
    def get_creation_number(self) -> int:
        return self.__creation_number