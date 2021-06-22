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
        # positions occupied by crosses and noughts
        self.playerPos = {'x': [], 'o': [], 'unoccupied': [1]*9}


    def getBoard(self):
        return self.spaces

    # places type ('x' if cross, 'o' if nought) on board at position pos
    def placeOnBoard(self, playerType, pos):
        self.spaces[pos] = playerType
        self.playerPos[playerType].append(pos)
        self.playerPos['unoccupied'][pos] = 0

    # assumes: playerType is 'x' (cross) or 'o' (nought)
    # returns: bool (true if finds numInRow in a row, false otherwise)
    #
    def threeInARow(self, player):

        soln = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        for x in soln:
            if all(y in self.playerPos[player] for y in x):
                return True

        return False

    # assumes: playerType is 'x' (cross) or 'o' (nought)
    # returns: int position of empty place on board where, if a cross/ nought
    # were placed there, would give that player 3 in a row
    # returns -1 if no such position exists
    #
    def twoInARow(self, player):
        soln = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        for x in soln:
            isInSoln = [y in self.playerPos[player] for y in x]

            if isInSoln == [True, True, False]:
                if self.playerPos['unoccupied'][x[2]]:
                    return x[2]
            elif isInSoln == [True, False, True]:
                if self.playerPos['unoccupied'][x[1]]:
                    return x[1]
            elif isInSoln == [False, True, True]:
                if self.playerPos['unoccupied'][x[0]]:
                    return x[0]

        return -1

    def isGameOver(self):
        # check for 3 crosses or noughts in a row - currPlayer wins (return 1)
        # check if board full - tie (return 0)
        # otherwise, game continues (return -1)
        if self.threeInARow('o'):
            return 1
        elif self.threeInARow('x'):
            return 2
        elif '' not in self.spaces:
            return 0
        else:
            return -1

    # randomly picks unoccupied board position for next move
    def nextMoveEasy(self):

        while 1:
            pos = np.random.randint(0, 9)

            if self.spaces[pos] == '':
                break

        self.placeOnBoard('o', pos)
        return pos

    # tries to get three in a row, otherwise blocks the player
    def nextMoveMed(self):
        twoInARow_comp = self.twoInARow('o')
        twoInARow_play = self.twoInARow('x')

        if twoInARow_comp >= 0:
            return twoInARow_comp
        elif twoInARow_play >= 0:
            return twoInARow_play


        return self.nextMoveEasy()

    # tries to get three in a row, otherwise blocks the player and tries to get 2 in a row
    def nextMoveHard(self):

        return 0
