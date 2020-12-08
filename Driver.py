#Utilizes the Observer Design Pattern found in ObserverClass.py

########################################
# NOTES BELOW #
########################################

#In creation of this file, REFERENCED:
    #https://www.youtube.com/watch?v=juSH7hmYUGA (timer tutorial)
    #https://docs.python.org/3/library/enum.html (Enums)

########################################
# IMPORTS BELOW #
########################################

#Import 3rd Party Libraries
import sys
import time
import pygame
from enum import Enum

#Import all from ObserverClass.py PlayerClass, EnemyClass, EnemyFactory and UIClass
from ObserverClass import *
from PlayerClass import *
from EnemyClass import *
from EnemyFactory import *
from UIClass import *

########################################
# ENUMS BELOW #
########################################

#Notes:
    #Used to keep track of the game state
class GameState(Enum):
    START = 0
    PLAYING = 1
    GAME_OVER = 2

#Notes:
    #Used to translate the internal representation of the board, boardWalls.txt into what the user/client sees
    #Not really an enum but a Class where all attributes are static
class boardWalls:
    WALL = "W"
    COIN = "C"
    PLAYER = "P"
    ENEMY = ["2", "3", "4", "5"]
    BACKGROUND = "B"

########################################
# DRIVER CLASS BELOW #
########################################

#Notes:
    #Below is the main Driver Class
class Driver:

    # Constructor
    def __init__(self):

        # Make a new instance of UIClass
        self.UIClass_obj = UIClass()

        # Create the board to be played on
        self.screen = self.UIClass_obj.setMode()

        # Create the timer that will keep running during the game
        self.timer = self.UIClass_obj.gameClock()

        # Set the playing state to True
        self.playing = True

        # Set the game state to start
        self.state = GameState.START

        # Set the size of the cell based on the UIClass.py file
        self.cell_width = self.UIClass_obj.board_width // self.UIClass_obj.columns
        self.cell_height = self.UIClass_obj.board_height // self.UIClass_obj.rows

        # Create the lists for the walls, coins, enemies, and enemy positions to fill and update over time
        self.walls = []
        self.enemy_list = []
        self.enemy_positions = []
        self.coins = []

        self.scorecap = 0
        self.numLives = 3

        # Create the player's position to start and where it will be updated over time
        self.player_position = None

        # Set the image of the board and the scale the game to it's size
        self.setgame()

        # Create our new player
        self.player = SingletonPlayer.getInstance(self, vec(self.player_position))
        self.player.resetDirection()

        # Populate our enemies array by creating enemies
        self.populateEnemies()

        # Set start time and elapsed time
        self.startTime = time.time()
        self.elapsedTime = 0

        # To keep track of which arrow-key is pressed for display purposes
        self.is_down = False
        self.is_up = False
        self.is_left = False
        self.is_right = False

    # Begin playing the game
    def runGame(self):

        # While the game is being played
        while self.playing:

            # If it is the start of the game
            if self.state == GameState.START:

                # Run the events class which corresponds to starting the program
                self.programStart()
                self.programDraw()

            # If it is currently during the game
            elif self.state == GameState.PLAYING:

                # Run the classes which corresponds to currently playing the game
                self.currentlyPlaying()
                self.currentUpdates()
                self.currentDrawing()

                # Increment countdown timer
                self.elapsedTime = int(time.time() - self.startTime)

            # If it is the end of the game
            elif self.state == GameState.GAME_OVER:

                # Run the events class which corresponds to ending the program
                self.endGame()
                self.endGameUpdate()
                self.endGameDraw()

            # Increment the timer
            self.timer.tick(self.UIClass_obj.fps)

        # Once everything is done quit the game
        self.UIClass_obj.quitGame()
        sys.exit()

    # Set the board image, and the grid that overlaps the board within the pygame window
    def setgame(self):

        board_width = self.UIClass_obj.board_width
        board_height = self.UIClass_obj.board_height

        self.background = self.UIClass_obj.loadBgImg('bg.png')
        self.background = self.UIClass_obj.scaleImg(self.background, board_width, board_height)

        # Create the playable board using the boardWalls.txt file
        with open("boardWalls.txt", 'r') as file:

            # For each row in the file, we need to go through and see what each item is
            for y, row in enumerate(file):

                # Check what the item is
                for x, col in enumerate(row):
                    
                    #Wall
                    if col == boardWalls.WALL:
                        self.walls.append(vec(x, y))

                    #Coin
                    elif col == boardWalls.COIN:
                        self.coins.append(vec(x, y))
                        self.scorecap += 1

                    #Player
                    elif col == boardWalls.PLAYER:
                        self.player_position = [x, y]

                    #Enemy
                    elif col in boardWalls.ENEMY:
                        self.enemy_positions.append([x, y])

                    # If the value is a B, then it's the background
                    elif col == boardWalls.BACKGROUND:
                        black = self.UIClass_obj.black
                        self.UIClass_obj.drawRect(self.background, black, (x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height))

    # Display the coins as a circle
    def coinDisplay(self):
        
        #Define outside of loop because they are constant
        surface = self.screen
        width = 5

        #For each coin in the coin list, draw the coin
        for coin in self.coins:
            center = (int(coin.x * self.cell_width) + self.cell_width // 2 + self.UIClass_obj.margin // 2, int(coin.y * self.cell_height) + self.cell_height // 2 + self.UIClass_obj.margin // 2)
            self.UIClass_obj.drawCircle(surface, self.UIClass_obj.coin_color, center, width)


    # Create enemies using Simple Factory (from EnemyClass.py)
    def populateEnemies(self):

        # Create an enemy factory object
        theFactory = EnemyFactory()

        # def CreateEnemy(self, type, Driver, pos, name, bit_state):
        for x, start_location in enumerate(self.enemy_positions):

            # Create a Blue Enemy
            # x will also be used to set the behavior bit for each enemy
            if x == 0:
                self.enemy_list.append(theFactory.CreateEnemy("Blue", self, vec(start_location), BlueEnemy, x))

            # Create a Orange Enemy
            elif x == 1:
                self.enemy_list.append(theFactory.CreateEnemy("Orange", self, vec(start_location), OrangeEnemy, x))

            # Create a Red Enemy (note enemy spelled incorrectly)
            elif x == 2:
                self.enemy_list.append(theFactory.CreateEnemy("Red", self, vec(start_location), RedEnemy, x))

            # Create a Pink Enemy (note enemy spelled incorrectly)
            elif x == 3:
                self.enemy_list.append(theFactory.CreateEnemy("Pink", self, vec(start_location), PinkEmemy, x))

    # Program start event
    def programStart(self):
        for event in pygame.event.get():

            # If the game is quit, set the playing state to False
            if event.type == pygame.QUIT:
                self.playing = False

            # If the user inputs a key, start the game
            if event.type == pygame.KEYDOWN:
                self.state = GameState.PLAYING

    # Draw the board
    def programDraw(self):
        self.screen.fill(self.UIClass_obj.black)
        window_width = self.UIClass_obj.window_width
        window_height = self.UIClass_obj.window_height
        font_style = self.UIClass_obj.start_font_style
        text_size = self.UIClass_obj.start_screen_text_size

        # Create the announcing observer
        announceObserver = ObserverClass()

        # Display Our Team Info
        announceObserver.observerDisplay('Pac-Man Recreation', self.screen, [window_width // 2, window_height // 2 - 75], text_size, self.UIClass_obj.blue, font_style, centered = True)
        announceObserver.observerDisplay('Max Macaluso, Rohan Suri, Sahib Bajwa', self.screen, [window_width // 2, window_height // 2 + 25], text_size, self.UIClass_obj.orange, font_style, centered = True)

        # Tell the player what button to push to start playing
        announceObserver.observerDisplay('Start: ANY BUTTON', self.screen, [window_width // 2, window_height // 2 + 125], text_size, self.UIClass_obj.white, font_style, centered = True)

        # Update the display
        self.UIClass_obj.updateDisplay()

    # Currently playing event (MOVEMENT)
    def currentlyPlaying(self):

        # For each event that occurs during the game
        for event in pygame.event.get():

            # If the event is a keystroke
            if event.type == pygame.KEYDOWN:

                # If the inputted keystroke is a left key, the player should move left and update button pressed display
                if event.key == pygame.K_LEFT:
                    self.player.movePlayer(vec(-1, 0))
                    self.updateArrowPressed("left")

                # If the inputted keystroke is a right key, the player should be moved right and update button pressed display
                if event.key == pygame.K_RIGHT:
                    self.player.movePlayer(vec(1, 0))
                    self.updateArrowPressed("right")

                # If the inputted keystroke is a up key, the player should be moved up and update button pressed display
                if event.key == pygame.K_UP:
                    self.player.movePlayer(vec(0, -1))
                    self.updateArrowPressed("up")

                # If the inputted keystroke is a down key, the player should be moved down and update button pressed display
                if event.key == pygame.K_DOWN:
                    self.player.movePlayer(vec(0, 1))
                    self.updateArrowPressed("down")

            # If the event is to quit the game, set the playing state to False and update button pressed display
            if event.type == pygame.QUIT:
                self.playing = False

    #Helper method to set which key is pressed for update button pressed display
        #Sets inputted value to be true and other 3 directions to False
    def updateArrowPressed(self, dir):
        if dir == "left":
            self.is_left = True
            self.is_right, self.is_down, self.is_up = (False, False, False)
        elif dir == "right":
            self.is_right = True
            self.is_left, self.is_down, self.is_up = (False, False, False)
        elif dir == "up":
            self.is_up = True
            self.is_right, self.is_down, self.is_left = (False, False, False)
        else:
            self.is_down = True
            self.is_right, self.is_up, self.is_left = (False, False, False)

    #Helper method to get which key is pressed for update button pressed display 
        #Returns string: "left", "right", "up", "down", "none"
    def getArrowPressed(self):
        if self.is_down:
            return "down"
        elif self.is_up:
            return "up"
        elif self.is_left:
            return "left"
        elif self.is_right:
            return "right"
        else:
            return "none"

    # Update while playing
    def currentUpdates(self):

        # Update the player's state
        self.player.updatePlayerState()
        for x in self.enemy_list:
            x.updateEnemyState()
            # self.player.alterScore(1000)

        # If the player and an enemy are in the same place, that means the player has died
        for x in self.enemy_list:

            if x.getPixPos() == self.player.getPixPos():
                # Remove a life since the player has died
                self.decrementLives()

        if self.player.returnScore() == self.scorecap:
            self.state = GameState.GAME_OVER

    # Draw the board during the game
    def currentDrawing(self):

        self.screen.fill(self.UIClass_obj.black)

        self.screen.blit(self.background, (self.UIClass_obj.margin // 2, self.UIClass_obj.margin // 2))

        # Draw the coins while the game is being played
        self.coinDisplay()

        # Create the announcing observer
        announceObserver = ObserverClass()

        # Display the score, time, and lives while the game is being played
        announceObserver.observerDisplay("Lives: " + str(self.numLives), self.screen, [150, 0], self.UIClass_obj.game_text_size, self.UIClass_obj.blue, self.UIClass_obj.start_font_style)
        announceObserver.observerDisplay("Time: " + str(self.elapsedTime), self.screen, [270, 0], self.UIClass_obj.game_text_size, self.UIClass_obj.blue, self.UIClass_obj.start_font_style)
        announceObserver.observerDisplay("Score: " + str(self.player.current_score), self.screen, [390, 0], self.UIClass_obj.game_text_size, self.UIClass_obj.blue, self.UIClass_obj.start_font_style)

        # Draw the player
        self.player.drawPlayer()

        # Draw the current button pressed
        announceObserver.observerDisplay("Button Pressed:", self.screen, [5, 250], 14, self.UIClass_obj.white, self.UIClass_obj.start_font_style)
        pressed_key = self.getArrowPressed()
        self.UIClass_obj.drawArrowKeys(pressed_key, self.screen, 35, 310, 25, 20)

        # Draw each enemy
        for enemy in self.enemy_list:
            enemy.draw()

        # Display the update
        self.UIClass_obj.updateDisplay()

    # Function for when a player loses a life
    def decrementLives(self):

        # Decrement the lives count by 1
        self.numLives -= 1

        # If the player has no lives, set the game state to over
        if self.numLives == 0:
            self.state = GameState.GAME_OVER

        # If the player still has lives
        else:

            # Set the grid position of the player as the starting position
            self.player.resetGridPos()

            # Set the pixel position of the player as the starting position
            self.player.resetPixPos()

            # Set the direction of the player to no direction
            self.player.resetDirection()
            
            for x in self.enemy_list:

                # Set the grid position of the enemy to the starting position
                x.current_grid_pos = vec(x.starting_pos)

                # Set the pixel position of the of the enemy to the starting position
                x.current_pix_pos = x.getPixPos()

                # Set the direction of the player to no direction
                x.direction *= 0

    # Event for when the game is over
    def endGame(self):

        for event in pygame.event.get():

            # If the user quits the game set the playing state to False
            if event.type == pygame.QUIT:
                self.playing = False

            # If the player presses space in the end game menu, reset the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

            # If the player preses escape in the end game menu, exit out of the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.playing = False

    # We don't need to really update anything if the program has just started
    def endGameUpdate(self):
        pass

    # If the game is over, we create an end game menu
    def endGameDraw(self):

        # Fill the entire window with a black background
        self.screen.fill(self.UIClass_obj.black)

        # Set the window dimensions
        window_width = self.UIClass_obj.window_width
        window_height = self.UIClass_obj.window_height

        # Create the announcing observer
        announceObserver = ObserverClass()

        announceObserver.observerDisplay("GAME OVER", self.screen, [window_width // 2, window_height // 2 - 250],  self.UIClass_obj.end_screen_text_size, self.UIClass_obj.red,  self.UIClass_obj.start_font_style, centered = True)

        # Score and Timer text
        announceObserver.observerDisplay("Score: " + str(self.player.returnScore()), self.screen, [window_width // 2, window_height // 2 + 90],  self.UIClass_obj.end_screen_text_size, self.UIClass_obj.blue, "arial", centered = True)
        elapsedTime2 = str(self.elapsedTime)
        announceObserver.observerDisplay("Time: " + str(elapsedTime2) + " Seconds", self.screen, [window_width // 2, window_height // 2 + 130],  self.UIClass_obj.end_screen_text_size, self.UIClass_obj.blue, "arial", centered = True)

        # Display the end game options
        announceObserver.observerDisplay("Play Again: SPACE", self.screen, [window_width // 2, window_height // 2 - 50],  self.UIClass_obj.end_screen_text_size, self.UIClass_obj.white, self.UIClass_obj.start_font_style, centered = True)
        announceObserver.observerDisplay("Quit Game: ESCAPE", self.screen, [window_width // 2, window_height // 2 - 10],  self.UIClass_obj.end_screen_text_size, self.UIClass_obj.white, self.UIClass_obj.start_font_style, centered = True)

        # Display thank you message
        announceObserver.observerDisplay("Thank you for playing!", self.screen, [window_width // 2, window_height // 2 - 150],  self.UIClass_obj.end_screen_text_size, self.UIClass_obj.orange, self.UIClass_obj.start_font_style, centered = True)

        # Update the display
        pygame.display.update()

    # Reset the game when appropriate
    def reset(self):

        # Set the lives back to 3
        self.numLives = 3

        # Set the score back to 0
        self.player.resetScore()

        # Set the player back to the starting location
        self.player.resetGridPos()

        # Set the player's pixel position back to the starting location
        self.player.resetPixPos()

        # Set the character's moving/facing direction to nothing
        self.player.resetDirection()
        for x in self.enemy_list:

            # Set the enemy's back to the starting location
            x.current_grid_pos = vec(x.starting_pos)

            # Set the enemy's pixel position back to the starting position
            x.current_pix_pos = x.getPixPos()

            # Set the enemy's moving/facing direction to nothing
            x.direction *= 0

        # Set the coins array back to empty
        self.coins = []

        # Set the elapsed time to 0
        self.elapsedTime = 0

        # Set the new start time
        self.startTime = time.time()

        # Reset the coin locations using the text file
        with open("boardWalls.txt", 'r') as file:
            #Traverse the file
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    #On a coin so add it
                    if char == boardWalls.COIN:
                        self.coins.append(vec(x, y))

        # Set the game state to playing
        self.state = GameState.PLAYING

########################################
# DRIVER BELOW #
########################################

if __name__ == '__main__':
    pygame.init()
    Driver().runGame()
