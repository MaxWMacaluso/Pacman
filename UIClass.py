########################################
# NOTES BELOW #
########################################

#This class is responsible for most things related to UI and pygame

########################################
# IMPORTS BELOW #
########################################

import pygame
vec = pygame.math.Vector2

########################################
# UICLASS BELOW #
########################################

class UIClass:
    def __init__(self):
        #COLORS
        self.player_color = (190, 194, 15)
        self.coin_color = (124, 123, 10)
        self.red = (255, 0, 0)
        self.pink = (255, 184, 255)
        self.white = (255, 255, 255)
        self.blue = (0, 255, 255)
        self.orange = (255, 184, 82)
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
        self.start_screen_text_size = 24
        self.game_text_size = 18
        self.end_screen_text_size = 36
        self.start_font_style = 'arial black'

    def drawCircle(self, surface, color, center, width):
        pygame.draw.circle(surface, color, center, width)

    # rect = [left, top, width, height]
    # 4 input params:
        # screen, color, (x,y,width,height), thickness
    def drawRect(self, surface, color, rect):
        pygame.draw.rect(surface, color, rect)

    #Method to display which key is pressed
    def drawArrowKeys(self, pressed_key, surface, x, y, width, height):
        if pressed_key == "up":
            pygame.draw.rect(surface, self.grey, (x, y, width, height)) #Left button
            pygame.draw.rect(surface, self.grey, (x + 30, y, width, height)) #Right button
            pygame.draw.rect(surface, self.white, (x + 15, y - 30, width, height)) #UP button
            pygame.draw.rect(surface, self.grey, (x + 15, y + 30, width, height)) #Down button
        elif pressed_key == "down": 
            pygame.draw.rect(surface, self.grey, (x, y, width, height)) #Left button
            pygame.draw.rect(surface, self.grey, (x + 30, y, width, height)) #Right button
            pygame.draw.rect(surface, self.grey, (x + 15, y - 30, width, height)) #Up button
            pygame.draw.rect(surface, self.white, (x + 15, y + 30, width, height)) #DOWN button
        elif pressed_key == "left": 
            pygame.draw.rect(surface, self.white, (x, y, width, height)) #LEFT button
            pygame.draw.rect(surface, self.grey, (x + 30, y, width, height)) #Right button
            pygame.draw.rect(surface, self.grey, (x + 15, y - 30, width, height)) #Up button
            pygame.draw.rect(surface, self.grey, (x + 15, y + 30, width, height)) #Down button
        elif pressed_key == "right": 
            pygame.draw.rect(surface, self.grey, (x, y, width, height)) #Left button
            pygame.draw.rect(surface, self.white, (x + 30, y, width, height)) #RIGHT button
            pygame.draw.rect(surface, self.grey, (x + 15, y - 30, width, height)) #Up button
            pygame.draw.rect(surface, self.grey, (x + 15, y + 30, width, height)) #Down button
        else:
            pygame.draw.rect(surface, self.grey, (x, y, width, height)) #Left button
            pygame.draw.rect(surface, self.grey, (x + 30, y, width, height)) #Right button
            pygame.draw.rect(surface, self.grey, (x + 15, y - 30, width, height)) #Up button
            pygame.draw.rect(surface, self.grey, (x + 15, y + 30, width, height)) #Down button

    def setMode(self):
        return (pygame.display.set_mode((self.window_width, self.window_height)))

    def gameClock(self):
        return (pygame.time.Clock())

    def quitGame(self):
        pygame.quit()

    def updateDisplay(self):
        pygame.display.update()

    def loadBgImg(self, bg_img):
        return (pygame.image.load(bg_img))

    def scaleImg(self, bg, width, height):
        return (pygame.transform.scale(bg, (width, height)))
