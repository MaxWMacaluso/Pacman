#Utilizes the Singleton Design Pattern

########################################
# NOTES BELOW #
########################################

#In creation of this file, REFERENCED:
    #https://python-patterns.guide/gang-of-four/singleton/ (Singleton)
    #https://www.cse.wustl.edu/~garnett/cse511a/code/project2/pacman_py.html (referenced code)
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
    #This is why self.[attribute] does not work
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
        #If previously uncreated, go in and create with correct starting params
        if cls._instance is None:
            
            #Create a new instance
            cls._instance = cls.__new__(cls)

            #Make a new instance of UIClass
            cls._instance.UIClass_obj = UIClass()
            
            #Save driver as driver
            cls._instance.driver = driver

            #Set Player speed to 2
            cls._instance.speed = 2

            #Save the current position in the grid based on what is passed in
            cls._instance.current_grid_pos = pos

            #Set the current pixel position based on where Player is in the grid
            cls._instance.current_pix_pos = cls._instance.getPixPos()
            
            #Save x, y starting position. Used in part when the game is reset
            cls._instance.starting_pos = [pos.x, pos.y]

            #Direction Player is facing. Starts to the right
            cls._instance.direction = vec(1, 0)

            cls._instance.stored_direction = None
            
            #Can move at first
            cls._instance.can_move = True

            #0 current score since 0 coins collected
            cls._instance.current_score = 0

        #Return the new instance created (if one was) or return the previously made one
        return cls._instance

    ########################################
    # 'MAIN' METHODS BELOW #
    ########################################

    #Sort of the driver method for this class, calls many other methods that help the Player instance do important things
    def updatePlayerState(self):
        #Set the current pixel position based off of current direciton and speed
        SingletonPlayer._instance.setCurrentPixPos()

        #Set if Player is able to move
        SingletonPlayer._instance.setCanMove()

        #Get the grid position given the pixel position
        SingletonPlayer._instance.pixPos_To_GridPos()

        #If on a coin, eat it
        SingletonPlayer._instance.eatCoin()

    #This method is responsible for drawing the player on the board
    def drawPlayer(self):
        #I do this to condense code
        instanceSingleton = SingletonPlayer._instance

        #Set variables for drawing the player which is a circle
        surface = instanceSingleton.driver.screen
        color = instanceSingleton.UIClass_obj.player_color
        center = (int(instanceSingleton.current_pix_pos.x), int(instanceSingleton.current_pix_pos.y))
        width = instanceSingleton.driver.cell_width // 2 - 2

        #Now that I have the values, actually go in and draw it
        instanceSingleton.UIClass_obj.drawCircle(surface, color, center, width)

    #Function that removes a coin and increments the score if the Player is on it according to current grid position
    def eatCoin(self):
        #To condense code
        instanceSingleton = SingletonPlayer._instance
        
        #If I am on a coin, remove it and increase score by 1
        if instanceSingleton.onCoin():
            SingletonPlayer._instance.removeCoin()
            SingletonPlayer._instance.alterScore(1)

    #Responsible and associated with the functionality of moving the Player
    def movePlayer(self, direction):
        SingletonPlayer._instance.stored_direction = direction

    
    ########################################
    # HELPER METHODS BELOW #
    ########################################

    #Returns the score of the Player based on how many coins have been eaten
    def returnScore(self):
        return SingletonPlayer._instance.current_score

    #Reset the grid position based off of the attribute starting_pos
    def resetGridPos(self):
        #To condense code
        instanceSingleton = SingletonPlayer._instance

        #Part that actually replaces the value with the starting position value
        instanceSingleton.current_grid_pos = vec(instanceSingleton.starting_pos)

    #Resets the pixel position based off the current grid position
        #Note: Should only be called after player current grid position is called
    def resetPixPos(self):
        instanceSingleton = SingletonPlayer._instance
        instanceSingleton.current_pix_pos = SingletonPlayer.getPixPos(self)

    #Very similiar to method above
    def resetDirection(self):
        instanceSingleton = SingletonPlayer._instance
        instanceSingleton.direction *= 0

    #Reset the Player instance's score to 0
    def resetScore(self):
        SingletonPlayer._instance.current_score = 0

    #Works with both pos and neg ints
    def alterScore(self, num):
        SingletonPlayer._instance.current_score += num

    #Returns a bool on whether or not a user is currently on a coin
    def onCoin(self):
        #Purely to condense code
        instanceSingleton = SingletonPlayer._instance
        down = (instanceSingleton.direction == vec(0, 1))
        up = (instanceSingleton.direction == vec(0, -1))
        right = instanceSingleton.direction == vec(1, 0)
        left = instanceSingleton.direction == vec(-1, 0)
        
        #If on a coin
        if instanceSingleton.current_grid_pos in instanceSingleton.driver.coins:
            
            #If vertical
            if instanceSingleton.yFun():
                #If down or up return true
                if down or up:
                    return True
            #If horizontal
            if instanceSingleton.xFun():
                #If right or left return true
                if right or left:
                    return True

        #None of the above are true so return False
        return False

    #Removes coin from map
    def removeCoin(self):
        #To condense code
        instanceSingleton = SingletonPlayer._instance

        #This is where I actually remove the coin from the GUI
        instanceSingleton.driver.coins.remove(instanceSingleton.current_grid_pos)

    #Returns a bool
    def canMove(self):

        #To condense code
        instanceSingleton = SingletonPlayer._instance
        for wall in instanceSingleton.driver.walls:

            #If going into a wall, cannot move so return false
            if vec(instanceSingleton.current_grid_pos + instanceSingleton.direction) == wall:
                return False

        #Else, I can move to return True
        return True

    def setCanMove(self):
        #To condense code
        instanceSingleton = SingletonPlayer._instance
        
        #If below method returns True
        if instanceSingleton.timeToMove():
            if instanceSingleton.stored_direction != None:
                instanceSingleton.direction = instanceSingleton.stored_direction
            #Lastly, update can_move
            instanceSingleton.can_move = instanceSingleton.canMove()

    #Returns a bool
    def timeToMove(self):
        #To condense code
        instanceSingleton = SingletonPlayer._instance
        right = (instanceSingleton.direction == vec(1, 0))
        left = (instanceSingleton.direction == vec(-1, 0))
        none = (instanceSingleton.direction == vec(0, 0))
        down = (instanceSingleton.direction == vec(0, 1))
        up = (instanceSingleton.direction == vec(0, -1))

        #Horizontal
        if instanceSingleton.xFun():
            #Right, left, or no direction; return True
            if right or left or none:
                return True
        #Vertical
        if instanceSingleton.yFun():
            #Down, up, or no direction; return True
            if down or up or none:
                return True
        #All other cases, return False
        return False

    #Method uses the current grid position (both x and y values) and cell width to calculate the Pixel Position
    def getPixPos(self):
        #To condense code
        instanceSingleton = SingletonPlayer._instance
        margin = instanceSingleton.UIClass_obj.margin

        #Below, set the x, y values which represent the pixel position
        x = (instanceSingleton.current_grid_pos[0] * instanceSingleton.driver.cell_width) + margin // 2 + instanceSingleton.driver.cell_width // 2
        y = (instanceSingleton.current_grid_pos[1] * instanceSingleton.driver.cell_height) + margin // 2 + instanceSingleton.driver.cell_height // 2
        
        #Return value
        return (vec(x, y))

    #Uses direction and speed to set current_pix_pos
    def setCurrentPixPos(self):
        #To condense code
        instanceSingleton = SingletonPlayer._instance

        #If the Player instance can move
        if instanceSingleton.can_move:
            
            #Update the current value of pix pos with the vector (direction and magnitude) (non scalar) value
            instanceSingleton.current_pix_pos += instanceSingleton.direction * instanceSingleton.speed

    #This method combines the two below to give both a X and Y result
    def pixPos_To_GridPos(self):
        #To condense code
        instanceSingleton = SingletonPlayer._instance

        #Now, call for both X and Y
        instanceSingleton.pixPos_To_GridPos_X()
        instanceSingleton.pixPos_To_GridPos_Y()

    #Method handles X value; converts the pixel position to the grid position using values from UIClass
    def pixPos_To_GridPos_X(self):
        #To condense the code
        instanceSingleton = SingletonPlayer._instance
        margin = instanceSingleton.UIClass_obj.margin

        #[0] is the x value
        #Here is where the magic actually happens
        instanceSingleton.current_grid_pos[0] = (instanceSingleton.current_pix_pos[0] - margin + instanceSingleton.driver.cell_width // 2) // instanceSingleton.driver.cell_width + 1

    #Method handles the Y value; converts the pixel position to the grid position using values from UIClass
    def pixPos_To_GridPos_Y(self):
        #Purely to condense code
        instanceSingleton = SingletonPlayer._instance
        margin = instanceSingleton.UIClass_obj.margin

        #[1] is the y value
        #Here is where the calculation is actually occuring
        instanceSingleton.current_grid_pos[1] = (instanceSingleton.current_pix_pos[1] - margin + instanceSingleton.driver.cell_height // 2) // instanceSingleton.driver.cell_height + 1

    #Returns a bool
    def xFun(self):
        #To condense code
        instanceSingleton = SingletonPlayer._instance
        margin = instanceSingleton.UIClass_obj.margin

        #Returns True or False based on whether LHS equals 0
        return (int(instanceSingleton.current_pix_pos.x + margin // 2) % instanceSingleton.driver.cell_width == 0)
    
    #Returns a bool
    def yFun(self):
        #To condense code
        instanceSingleton = SingletonPlayer._instance
        margin = instanceSingleton.UIClass_obj.margin

        #Returns True or False based on whether LHS equals 0
        return (int(instanceSingleton.current_pix_pos.y + margin // 2) % instanceSingleton.driver.cell_height == 0)
