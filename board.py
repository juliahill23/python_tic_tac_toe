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
        self.corners = [0, 2, 6, 8]


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
        # all possible ways to get 3 in a row
        soln = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        # check to see if player has 3 in a row
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
        # all possible ways to get 3 in a row
        soln = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        # check to see if player has 2 in a row and that getting 3 in a row is possible
        for x in soln:
            is_in_soln = [y in self.playerPos[player] for y in x]

            if is_in_soln == [True, True, False]:
                if self.playerPos['unoccupied'][x[2]]:
                    return x[2]
            elif is_in_soln == [True, False, True]:
                if self.playerPos['unoccupied'][x[1]]:
                    return x[1]
            elif is_in_soln == [False, True, True]:
                if self.playerPos['unoccupied'][x[0]]:
                    return x[0]

        # return -1 if can't get 3 in a row
        return -1

    # returns a list of all keys of dictionary dic with value value
    def getAllKeysWithValue(self, dic, value):
        result = []
        for key, val in dic.items():
            if val == value:
                result.append(key)
        return result

    # returns list of all positions on board which would result in player getting 2 in a row
    def getTwoInARow(self, player):
        soln = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        # tracks the value of each position on the board, the more possible 2s, the higher the value
        # of the position in the dictionary
        counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

        for x in soln:
            is_in_soln = [y in self.playerPos[player] for y in x]

            if is_in_soln == [True, False, False]:
                if self.playerPos['unoccupied'][x[1]] and self.playerPos['unoccupied'][x[2]]:
                    counts[x[1]] += 1
                    counts[x[2]] += 1
            elif is_in_soln == [False, False, True]:
                if self.playerPos['unoccupied'][x[0]] and self.playerPos['unoccupied'][x[1]]:
                    counts[x[1]] += 1
                    counts[x[0]] += 1
            elif is_in_soln == [False, True, False]:
                if self.playerPos['unoccupied'][x[0]] and self.playerPos['unoccupied'][x[2]]:
                    counts[x[0]] += 1
                    counts[x[2]] += 1
        # gets first value in dictionary with highest value
        max_key = max(counts, key=counts.get)
        # if no viable options, return [-1]
        if max_key == 0 and counts[0] == 0:
            return [-1]
        # if other keys exist with the same value, return them as well
        else:
            return self.getAllKeysWithValue(counts, counts[max_key])

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
        two_in_a_row_comp = self.twoInARow('o')
        two_in_a_row_play = self.twoInARow('x')

        if two_in_a_row_comp >= 0:
            return two_in_a_row_comp
        elif two_in_a_row_play >= 0:
            return two_in_a_row_play


        return self.nextMoveEasy()

    # tries to get three in a row, otherwise blocks the player and tries to get 2 in a row
    # if it is the first move and the player chose a corner, choose the middle.
    def nextMoveHard(self):

        two_in_a_row_comp = self.twoInARow('o')
        two_in_a_row_play = self.twoInARow('x')
        get_two_in_a_row_comp = self.getTwoInARow('o')
        get_two_in_a_row_play = self.getTwoInARow('x')

        # if 'o' can make three in a row, make that move
        if two_in_a_row_comp >= 0:
            return two_in_a_row_comp
        # otherwise, if 'o' can block 'x' from making 3 in a row, make that move
        elif two_in_a_row_play >= 0:
            return two_in_a_row_play
        # otherwise, find optimal place to get 2 in a row, find optimal place for opponent to get 2 in a row
        # and if there is union, select that number
        elif get_two_in_a_row_comp[0] >= 0 and get_two_in_a_row_play[0] >= 0:
            for pos in get_two_in_a_row_comp:
                if pos in get_two_in_a_row_play:
                    return pos
        # otherwise, choose a move that gets 2 in a row
        elif get_two_in_a_row_comp[0] >= 0:
            return np.random.choice(get_two_in_a_row_comp)
        # if first player move is in corner, pick middle of board
        elif not self.playerPos['o'] and self.playerPos['x'][0] in self.corners and self.playerPos['unoccupied'][4]:
            return 4

        # should probably never get here other than for the first move,
        # but if all conditions fail, choose random pos
        return self.nextMoveEasy()
