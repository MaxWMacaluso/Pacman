#Utilizes the Singleton Design Pattern

########################################
# NOTES BELOW #
########################################

#In creation of this file, REFERENCED:
    #https://python-patterns.guide/gang-of-four/singleton/ (Singleton)
    #https://www.cse.wustl.edu/~garnett/cse511a/code/project2/pacman_py.html (referenced code)
    #https://github.com/a-plus-coding/pacman-with-python (referenced code)
    #http://zetcode.com/javagames/pacman/ (referenced code)

########################################
# IMPORTS BELOW #
########################################

#Import all from UIClass
from UIClass import *

########################################
# SINGLETONPLAYER CLASS BELOW #
########################################

#Notes: 
    #Interesting note, theoretically, a SingletonPlayer instance would have no attributes (essentially null); however, static _instance is what is defined
    #This is why self.[attributes] does not work
class SingletonPlayer:
    #Static Singleton instance
    _instance = None

    #Constructor
    def __init__(self):
        raise RuntimeError('This is a Singleton; call SingletonPlayer.getInstance() instead!')

    #Create a new instance and return it if none existed; else, return made class variable (static) _instance
    #Similiar to a static method
    @classmethod
    def getInstance(cls, driver, pos):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.UIClass_obj = UIClass() #Make a new instance of UIClass
            cls._instance.driver = driver
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
        SingletonPlayer._instance.setCurrentPixPos()
        SingletonPlayer._instance.setCanMove()
        SingletonPlayer._instance.pixPos_To_GridPos()
        SingletonPlayer._instance.eatCoin()

    def drawPlayer(self):
        instanceSingleton = SingletonPlayer._instance
        surface = instanceSingleton.driver.screen
        color = instanceSingleton.UIClass_obj.player_color
        center = (int(instanceSingleton.current_pix_pos.x), int(instanceSingleton.current_pix_pos.y))
        width = instanceSingleton.driver.cell_width // 2 - 2
        instanceSingleton.UIClass_obj.drawCircle(surface, color, center, width)

    def drawLives(self):
        instanceSingleton = SingletonPlayer._instance
        surface = instanceSingleton.driver.screen
        color = instanceSingleton.UIClass_obj.player_color
        radius = 7
        #Repeats to number of num_lives
        for x in range(instanceSingleton.num_lives):
            x = int(30 + 20 * x)
            y = int(instanceSingleton.UIClass_obj.window_height - 15)
            center = (x, y)
            instanceSingleton.UIClass.drawCircle(surface, color, center, radius)

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
        if instanceSingleton.current_grid_pos in instanceSingleton.driver.coins:
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
        instanceSingleton.driver.coins.remove(instanceSingleton.current_grid_pos)

    #Returns a bool
    def canMove(self):
        instanceSingleton = SingletonPlayer._instance
        for wall in instanceSingleton.driver.walls:
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
            #Right, left, or no direction
            if instanceSingleton.direction == vec(1, 0) or instanceSingleton.direction == vec(-1, 0) or instanceSingleton.direction == vec(0, 0):
                return True
        if instanceSingleton.yFun():
            #Up, down, or no direction
            if instanceSingleton.direction == vec(0, 1) or instanceSingleton.direction == vec(0, -1) or instanceSingleton.direction == vec(0, 0):
                return True
        #TODO: may need to fix logic
        return False

    def getPixPos(self):
        instanceSingleton = SingletonPlayer._instance
        margin = instanceSingleton.UIClass_obj.margin

        #TODO: 
        x = (instanceSingleton.current_grid_pos[0] * instanceSingleton.driver.cell_width) + margin // 2 + instanceSingleton.driver.cell_width // 2
        y = (instanceSingleton.current_grid_pos[1] * instanceSingleton.driver.cell_height) + margin // 2 + instanceSingleton.driver.cell_height // 2
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
        margin = instanceSingleton.UIClass_obj.margin

        #TODO:
        instanceSingleton.current_grid_pos[0] = (instanceSingleton.current_pix_pos[0] - margin + instanceSingleton.driver.cell_width // 2) // instanceSingleton.driver.cell_width + 1

    def pixPos_To_GridPos_Y(self):
        instanceSingleton = SingletonPlayer._instance
        margin = instanceSingleton.UIClass_obj.margin
        instanceSingleton.current_grid_pos[1] = (instanceSingleton.current_pix_pos[1] - margin + instanceSingleton.driver.cell_height // 2) // instanceSingleton.driver.cell_height + 1

    #Returns a bool
    def xFun(self):
        instanceSingleton = SingletonPlayer._instance
        margin = instanceSingleton.UIClass_obj.margin

        #TODO:
        return (int(instanceSingleton.current_pix_pos.x + margin // 2) % instanceSingleton.driver.cell_width == 0)
    
    #Returns a bool
    def yFun(self):
        instanceSingleton = SingletonPlayer._instance
        margin = instanceSingleton.UIClass_obj.margin

        #TODO:
        return (int(instanceSingleton.current_pix_pos.y + margin // 2) % instanceSingleton.driver.cell_height == 0)

    # Sahib's methods for Driver.py
    def returnScore(self):
        return SingletonPlayer._instance.current_score

    def resetGridPos(self):
        instanceSingleton = SingletonPlayer._instance
        instanceSingleton.current_grid_pos = vec(instanceSingleton.starting_pos)

    def resetPixPos(self):
        instanceSingleton = SingletonPlayer._instance
        instanceSingleton.current_pix_pos = SingletonPlayer.getPixPos(self)

    def resetDirection(self):
        instanceSingleton = SingletonPlayer._instance
        instanceSingleton.direction *= 0

    def resetScore(self):
        SingletonPlayer._instance.current_score = 0
