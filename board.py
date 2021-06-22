import numpy as np
class Board:
    def __init__(self):
        # space on board is:
        # - 0 if unoccupied
        # - 1 if cross
        # - 2 if nought
        # initialized as 3x3 unoccupied board, with indexes describing pos:
        # 0 | 1 | 2
        #---+---+---
        # 3 | 4 | 5
        #---+---+---
        # 6 | 7 | 8
        self.spaces = ['' for x in range(9)]
        self.playerPos = {'x': [], 'o': []}  # positions occupied by crosses and noughts

    def getBoard(self):
        return self.spaces

    # places type ('x' if cross, 'o' if nought) on board at position pos
    def placeOnBoard(self, playerType, pos):
        self.spaces[pos] = playerType
        self.playerPos[playerType].append(pos)


    # assumes: playerType is 'x' (cross) or 'o' (nought), numInRow is 2 or 3
    # returns: bool (true if finds numInRow in a row, false otherwise)
    #
    def inARow(self, numInRow, player):
        if numInRow == 3:
            soln = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                    [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

            for x in soln:
                if all(y in self.playerPos[player] for y in x):
                    return True

            return False


    def isGameOver(self, currPlayer):

        # check for 3 crosses or noughts in a row - currPlayer wins (return 1)
        # check if board full - tie (return 0)
        # otherwise, game continues (return -1)
        if self.inARow(3, 'o'):
            return 1
        elif self.inARow(3, 'x'):
            return 2
        elif '' not in self.spaces:
            return 0
        else:
            return -1

    def playNextMoveEasy(self):

        while 1:
            pos = np.random.randint(0, 9)

            if self.spaces[pos] == '':
                break

        self.placeOnBoard('o', pos)

    #def findNextMoveMedium(self):
    #def findNextMoveHard(self):

