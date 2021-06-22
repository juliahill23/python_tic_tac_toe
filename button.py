import pygame as pg

pg.font.init()
menu_font = pg.font.Font(None, 30)


class Button:
    hovered = False

    def __init__(self, text, pos, screen):
        self.text = text
        self.pos = pos
        self.screen = screen

        self.rend = menu_font.render(self.text, True, self.get_color())
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

        self.draw()

    def draw(self):
        self.rend = menu_font.render(self.text, True, self.get_color())
        self.screen.blit(self.rend, self.rect)

    def get_color(self):
        if self.hovered:
            return (255, 255, 41)
        else:
            return (255, 255, 255)

