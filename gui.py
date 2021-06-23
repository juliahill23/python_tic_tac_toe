import pygame as pg
import sys
import time
from board import Board
from button import Button


currPlayer = 'x'    # current Player
board = Board()     # initializes Board object

winner = -1         # -1 if game ongoing
                    # 0 if game over, tie
                    # 1 if gamer over, 'x' wins
                    # 2 if game over, 'o' wins

# game difficulty, 'easy', 'med', or 'hard'
gamemode = ''

# constants for pygame display
width = 400
height = 400
fps = 30

# colour constants
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 41)

# initialize clock
CLOCK = pg.time.Clock()

# initializing the pygame window
pg.init()

# load images
x_img = pg.image.load("x.png")
o_img = pg.image.load("o.png")

# build the infrastructure of the display
screen = pg.display.set_mode((width, height + 100), 0, 32)

pg.display.set_caption("Tic Tac Toe")

# resizing images
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))


def select_difficulty_screen():
    global screen, gamemode
    # displaying over the screen
    # screen.blit(initiating_window, (0, 0))

    # fills background with black
    screen.fill(black)

    # initialize buttons (position, font, color ect.)
    buttons = [Button("EASY", (width / 2 - 20, 500 - 400), screen),
               Button("MEDIUM", (width / 2 - 32, 500 - 300), screen),
               Button("HARD", (width / 2 - 20, 500 - 200), screen)]

    display_menu = True

    while display_menu:
        # internally process pygame event handlers
        pg.event.pump()

        # get key / mouse events
        for event in pg.event.get():
            # if user presses exit button, quit game
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # if user clicks on one of the buttons, set difficulty
            # then exit while loop
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if buttons[0].rect.collidepoint(pos):
                    gamemode = 'easy'
                    # exit while loop
                    display_menu = False
                elif buttons[1].rect.collidepoint(pos):
                    gamemode = 'med'
                    display_menu = False
                elif buttons[2].rect.collidepoint(pos):
                    gamemode = 'hard'
                    display_menu = False

        # if mouse hovers over button, change button color
        for button in buttons:
            if button.rect.collidepoint(pg.mouse.get_pos()):
                button.hovered = True
            else:
                button.hovered = False
            button.draw()

        # update display
        pg.display.update()
        CLOCK.tick(fps)

    time.sleep(0.25)


def game_init_window():
    # initializes screen, allows player to select difficulty
    select_difficulty_screen()

    # updating the display
    screen.fill(black)

    # drawing vertical lines
    pg.draw.line(screen, white, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, white, (width / 3 * 2, 0), (width / 3 * 2, height), 7)

    # drawing horizontal lines
    pg.draw.line(screen, white, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, white, (0, height / 3 * 2), (width, height / 3 * 2), 7)
    game_status()


def game_status():
    message = None

    # check win status
    if winner < 0:
        if currPlayer == 'x':
            message = "Your Turn"
        else:
            message = currPlayer.upper() + "'s Turn"
    elif winner == 1:
        message = "You lost "
    elif winner == 2:
        message = "You won !"
    elif winner == 0:
        message = "Game Draw !"

    # setting a font object
    font = pg.font.Font(None, 30)

    # setting the font properties like
    # color and width of the text
    if message:
        text = font.render(message, True, (255, 255, 255))

        # copy the rendered message onto the board
        # creating a small block at the bottom of the main display
        screen.fill((0, 0, 0), (0, 400, 500, 100))
        text_rect = text.get_rect(center=(width / 2, 500 - 50))
        screen.blit(text, text_rect)
        pg.display.update()


def update_Board(pos):
    global currPlayer
    pos_x, pos_y = 0, 0

    if pos in [0, 1, 2]:                # first row
        pos_y = 30
    elif pos in [3, 4, 5]:              # second row
        pos_y = width / 3 + 30
    elif pos in [6, 7, 8]:              # third row
        pos_y = width / 3 * 2 + 30

    if pos in [0, 3, 6]:                # first col
        pos_x = 30
    elif pos in [1, 4, 7]:              # second col
        pos_x = height / 3 + 30
    elif pos in [2, 5, 8]:              # third col
        pos_x = height / 3 * 2 + 30

    # update board with new move
    board.placeOnBoard(currPlayer, pos)

    if currPlayer == 'x':

        # pasting x_img over the screen
        # at a coordinate position of
        # (pos_x, pos_y) defined in the
        # above code
        screen.blit(x_img, (pos_x, pos_y))
        # change player
        currPlayer = 'o'

    else:
        screen.blit(o_img, (pos_x, pos_y))
        currPlayer = 'x'

    # update display
    pg.display.update()


def user_click():
    global winner, currPlayer
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()

    # determine position on board
    if (x < width / 3) and (y < height / 3):                    # col 1, row 1
        pos = 0
    elif (x < width / 3 * 2) and (y < height / 3):              # col 2, row 1
        pos = 1
    elif (x < width) and (y < height / 3):                      # col 3, row 1
        pos = 2
    elif (x < width / 3) and (y < height / 3 * 2):              # col 1, row 2
        pos = 3
    elif (x < width / 3 * 2) and (y < height / 3 * 2):          # col 2, row 2
        pos = 4
    elif (x < width) and (y < height / 3 * 2):                  # col 3, row 2
        pos = 5
    elif (x < width / 3) and (y < height):                      # col 1, row 3
        pos = 6
    elif (x < width / 3 * 2) and (y < height):                  # col 2, row 3
        pos = 7
    elif (x < width) and (y < height):                          # col 3, row 3
        pos = 8

    # draw the images at the desired positions, update board
    if board.getBoard()[pos] == '':

        update_Board(pos)
        # check if game has been won / is over
        winner = board.isGameOver()
        game_status()


def reset_game():
    # reset everything to initial values
    global board, winner, currPlayer, gamemode
    time.sleep(2)
    gamemode = ''
    currPlayer = 'x'
    winner = -1
    board = Board()
    game_init_window()
    game_status()


if __name__ == '__main__':
    game_init_window()
    board.twoInARow(currPlayer)

    while True:

        for event in pg.event.get():
            # quit game if user selects quit button
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # if user clicks on unoccupied board position and it
            # is the users turn, updates the board and draws the move
            elif event.type == pg.MOUSEBUTTONDOWN and currPlayer == 'x':

                user_click()
                # if game is over, restart the game
                if winner == 0 or winner == 1 or winner == 2:
                    reset_game()

        # if it is the computer's turn
        if currPlayer == 'o':
            time.sleep(0.5)
            # get computer's next move, based on game difficulty
            if gamemode == 'easy':
                pos = board.nextMoveEasy()
            elif gamemode == 'med':
                pos = board.nextMoveMed()
            elif gamemode == 'hard':
                pos = board.nextMoveHard()

            # draw the move, update board
            update_Board(pos)
            # check to see if game has ended
            winner = board.isGameOver()
            # update game status text on screen
            game_status()
            # if game is over, reset the game
            if winner == 0 or winner == 1 or winner == 2:
                reset_game()

        pg.display.update()
        CLOCK.tick(fps)
