import pygame as pg

# initialize pygame font module
pg.font.init()
menu_font = pg.font.Font(None, 30)


class Button:

    # flag to change color if mouse hovers over button
    hovered = False

    def __init__(self, text, pos, screen):

        self.text = text
        self.pos = pos
        self.screen = screen

        # render font
        self.rend = menu_font.render(self.text, True, self.get_color())

        # create rectangle for interacting with button
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

        self.draw()

    def draw(self):
        # draw button on screen
        self.rend = menu_font.render(self.text, True, self.get_color())
        self.screen.blit(self.rend, self.rect)

    def get_color(self):
        if self.hovered:
            return (255, 255, 41)  # yellow if hovered
        else:
            return (255, 255, 255) # white otherwise
