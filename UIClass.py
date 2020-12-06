#This class is responsible for most things related to UI and pygame

import pygame
vec = pygame.math.Vector2

class UIClass:
    def __init__(self):
        #COLORS
        self.player_color = (190, 194, 15)
        self.coin_color = (124, 123, 10)
        self.red = (208, 22, 22)
        self.white = (255, 255, 255)
        self.grey = (107, 107, 107)
        self.black = (0, 0, 0)

        #SCREEN
        self.margin = 50
        self.window_width = 610
        self.window_height = 670
        self.board_width = self.window_width - self.margin
        self.board_height = self.window_height - self.margin

        #DEFAULT GAME SPEED
        self.fps = 60

        self.rows = 30
        self.columns = 28

        #FONT 
        self.start_screen_text_size = 18
        self.start_font_style = 'arial black'

    def drawCircle(self, surface, color, center, width):
        pygame.draw.circle(surface, color, center, width)

    def drawRect(self, surface, color, rect):
        pygame.draw.rect(surface, color, rect)

    def setMode(self):
        return (pygame.display.set_mode((self.window_width, self.window_height)))

    def gameClock(self):
        return (pygame.time.Clock())

    def quitGame(self):
        pygame.quit()

    def updateDisplay(self):
        pygame.display.update()

    def loadImg(self, bg_img):
        return (pygame.image.load(bg_img))

    def scaleImg(self, bg, width, height):
        return (pygame.transform.scale(bg, (width, height)))
