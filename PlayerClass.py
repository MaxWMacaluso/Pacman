#Utilizes the Singleton Design Pattern
#In creation of this file, referenced:
    #https://python-patterns.guide/gang-of-four/singleton/
    #https://www.cse.wustl.edu/~garnett/cse511a/code/project2/pacman_py.html
    #https://github.com/a-plus-coding/pacman-with-python

import pygame

from constants import *
vec = pygame.math.Vector2

#Interesting note, theoretically, a SingletonPlayer instance would have no attributes (essentially null); however, static _instance is what is defined.
#This is why self.[attributes] does not work
class SingletonPlayer:
    #Static Singleton instance
    _instance = None

    #Constructor
    def __init__(self):
        raise RuntimeError('This is a Singleton; call getInstance() instead!')

    #Create a new instance and return it if none existed; else, return made class variable (static) _instance
    @classmethod
    def getInstance(cls, app, pos):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.app = app
            cls._instance.speed = 2
            cls._instance.num_lives = 1
            cls._instance.current_grid_pos = pos
            cls._instance.current_pix_pos = cls._instance.getPixPos()
            cls._instance.starting_pos = [pos.x, pos.y]
            cls._instance.direction = vec(1, 0)
            cls._instance.stored_direction = None
            cls._instance.can_move = True
            cls._instance.current_score = 0
        return cls._instance

    def updatePlayerState(self):
        instanceSingleton = SingletonPlayer._instance
        instanceSingleton.setCurrentPixPos()
        instanceSingleton.setCanMove()
        instanceSingleton.pixPos_To_GridPos()
        instanceSingleton.eatCoin()

    def drawPlayer(self):
        instanceSingleton = SingletonPlayer._instance
        surface = instanceSingleton.app.screen
        center = (int(instanceSingleton.current_pix_pos.x), int(instanceSingleton.current_pix_pos.y))
        width = instanceSingleton.app.cell_width // 2 - 2
        pygame.draw.circle(surface, PLAYER_COLOUR, center, width)

    def drawLives(self):
        instanceSingleton = SingletonPlayer._instance
        surface = instanceSingleton.app.screen
        radius = 7
        #Repeats to number of num_lives
        for x in range(instanceSingleton.num_lives):
            center = (int(30 + 20 * x), int(WINDOW_HEIGHT - 15))
            pygame.draw.circle(surface, PLAYER_COLOUR, center, radius)

    def eatCoin(self):
        instanceSingleton = SingletonPlayer._instance
        if instanceSingleton.onCoin():
            SingletonPlayer._instance.removeCoin()
            SingletonPlayer._instance.alterScore(1)

    def movePlayer(self, direction):
        SingletonPlayer._instance.stored_direction = direction

    
    ########################################
    # HELPER METHODS BELOW #
    ########################################

    #Works with both pos and neg ints
    def alterScore(self, num):
        SingletonPlayer._instance.current_score += num

    #TODO: May need to fix logic
    #Returns a bool
    def onCoin(self):
        instanceSingleton = SingletonPlayer._instance
        #If on a coin
        if instanceSingleton.current_grid_pos in instanceSingleton.app.coins:
            #Vertical
            if instanceSingleton.yFun():
                #If looking up or down
                if instanceSingleton.direction == vec(0, 1) or instanceSingleton.direction == vec(0, -1):
                    return True
            #Horizontal
            if instanceSingleton.xFun():
                if instanceSingleton.direction == vec(1, 0) or instanceSingleton.direction == vec(-1, 0):
                    return True
        return False

    #Removes coin from map
    def removeCoin(self):
        instanceSingleton = SingletonPlayer._instance
        instanceSingleton.app.coins.remove(instanceSingleton.current_grid_pos)

    #Returns a bool
    def canMove(self):
        instanceSingleton = SingletonPlayer._instance
        for wall in instanceSingleton.app.walls:
            if vec(instanceSingleton.current_grid_pos + instanceSingleton.direction) == wall:
                return False
        return True

    def setCanMove(self):
        instanceSingleton = SingletonPlayer._instance
        if instanceSingleton.timeToMove():
            if instanceSingleton.stored_direction != None:
                instanceSingleton.direction = instanceSingleton.stored_direction
            instanceSingleton.can_move = instanceSingleton.canMove()

    #Returns a bool
    def timeToMove(self):
        instanceSingleton = SingletonPlayer._instance
        if instanceSingleton.xFun():
            if instanceSingleton.direction == vec(1, 0) or instanceSingleton.direction == vec(-1, 0) or instanceSingleton.direction == vec(0, 0):
                return True
        if instanceSingleton.yFun():
            if instanceSingleton.direction == vec(0, 1) or instanceSingleton.direction == vec(0, -1) or instanceSingleton.direction == vec(0, 0):
                return True
        #TODO: may need to fix logic
        return False

    def getPixPos(self):
        instanceSingleton = SingletonPlayer._instance
        x = (instanceSingleton.current_grid_pos[0] * instanceSingleton.app.cell_width) + TOP_BOTTOM_MARGIN // 2 + instanceSingleton.app.cell_width // 2
        y = (instanceSingleton.current_grid_pos[1] * instanceSingleton.app.cell_height) + TOP_BOTTOM_MARGIN // 2 + instanceSingleton.app.cell_height // 2
        return (vec(x, y))

    #Uses direction and speed to set current_pix_pos
    def setCurrentPixPos(self):
        instanceSingleton = SingletonPlayer._instance
        if instanceSingleton.can_move:
            instanceSingleton.current_pix_pos += instanceSingleton.direction * instanceSingleton.speed

    def pixPos_To_GridPos(self):
        instanceSingleton = SingletonPlayer._instance
        instanceSingleton.pixPos_To_GridPos_X()
        instanceSingleton.pixPos_To_GridPos_Y()

    def pixPos_To_GridPos_X(self):
        instanceSingleton = SingletonPlayer._instance
        instanceSingleton.current_grid_pos[0] = (instanceSingleton.current_pix_pos[0] - TOP_BOTTOM_MARGIN + instanceSingleton.app.cell_width // 2) // instanceSingleton.app.cell_width + 1

    def pixPos_To_GridPos_Y(self):
        instanceSingleton = SingletonPlayer._instance
        instanceSingleton.current_grid_pos[1] = (instanceSingleton.current_pix_pos[1] - TOP_BOTTOM_MARGIN + instanceSingleton.app.cell_height // 2) // instanceSingleton.app.cell_height + 1

    #Returns a bool
    def xFun(self):
        return (int(SingletonPlayer._instance.current_pix_pos.x + TOP_BOTTOM_MARGIN // 2) % SingletonPlayer._instance.app.cell_width == 0)
    
    #Returns a bool
    def yFun(self):
        return (int(SingletonPlayer._instance.current_pix_pos.y + TOP_BOTTOM_MARGIN // 2) % SingletonPlayer._instance.app.cell_height == 0)