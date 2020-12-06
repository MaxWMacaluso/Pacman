########################################
# NOTES BELOW #
########################################

#Utilizes the Observer Design Pattern

#In creation of this file, REFERENCED:
    #https://www.youtube.com/watch?v=juSH7hmYUGA (timer tutorial)
    #https://docs.python.org/3/library/enum.html (Enums)

########################################
# IMPORTS BELOW #
########################################

#Import 3rd Party Libraries
import sys
import time
from enum import Enum

#Import all from PlayerClass, EnemyClass, and UIClass
from PlayerClass import *
from EnemyClass import *
from UIClass import *

########################################
# ENUM BELOW #
########################################

#Notes:
    #Used to keep track of the game state
class GameState(Enum):
    START = 0
    PLAYING = 1
    GAME_OVER = 2

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

        # Set the game state to 'start'
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

        # Create the playable board using the walls.txt file
        with open("board_walls.txt", 'r') as file:

            # For each row in the file, we need to go through and see what each item is
            for y, row in enumerate(file):

                # Check what the item is
                for x, col in enumerate(row):

                    # If the value is a 1, it's a wall
                    if col == "1":
                        self.walls.append(vec(x, y))

                    # If the value is a C, it's a coin
                    elif col == "C":
                        self.coins.append(vec(x, y))
                        self.scorecap += 1

                    # If the value is a P, it's a player
                    elif col == "P":
                        self.player_position = [x, y]

                    # If the value is 2, 3, 4, or 5, it's an enemy
                    elif col in ["2", "3", "4", "5"]:
                        self.enemy_positions.append([x, y])

                    # If the value is a B, then it's the background
                    elif col == "B":
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = GameState.PLAYING

    # Draw the board
    def programDraw(self):

        self.screen.fill(self.UIClass_obj.black)
        window_width = self.UIClass_obj.window_width
        window_height = self.UIClass_obj.window_height
        font_style = self.UIClass_obj.start_font_style
        text_size = self.UIClass_obj.start_screen_text_size

        # Create the announcing observer
        announceObserver = observerMethod()

        # Tell the player what button to push to start playing
        announceObserver.observerDisplay('Press SPACE to start', self.screen, [window_width // 2, window_height // 2 - 75], 35, (170, 132, 58), font_style, centered=True)

        # Display Our Team Info
        announceObserver.observerDisplay('Pac Man Recreation', self.screen, [window_width // 2, window_height // 2 + 25], 25, (44, 167, 198), font_style, centered=True)
        announceObserver.observerDisplay('Max Macaluso, Rohan Suri, Sahib Bajwa', self.screen, [window_width // 2, window_height // 2 + 75], text_size, (55, 155, 98), font_style, centered=True)

        # Update the display
        self.UIClass_obj.updateDisplay()

    # Currently playing event (MOVEMENT)
    def currentlyPlaying(self):

        # For each event that occurs during the game
        for event in pygame.event.get():

            # If the event is a keystroke
            if event.type == pygame.KEYDOWN:

                # If the inputted keystroke is a left key, the player should move left
                if event.key == pygame.K_LEFT:
                    self.player.movePlayer(vec(-1, 0))

                # If the inputted keystroke is a right key, the player should be moved right
                if event.key == pygame.K_RIGHT:
                    self.player.movePlayer(vec(1, 0))

                # If the inputted keystroke is a up key, the player should be moved up
                if event.key == pygame.K_UP:
                    self.player.movePlayer(vec(0, -1))

                # If the inputted keystroke is a down key, the player should be moved down
                if event.key == pygame.K_DOWN:
                    self.player.movePlayer(vec(0, 1))

            # If the event is to quit the game, set the playing state to False
            if event.type == pygame.QUIT:
                self.playing = False

    # Update while playing
    def currentUpdates(self):

        # Update the player's state
        self.player.updatePlayerState()

        # TODO: Update each enemy's state (not working)
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
        announceObserver = observerMethod()

        # Display the score while the game is being played
        announceObserver.observerDisplay('SCORE: {}'.format(self.player.current_score), self.screen, [60, 0], 18, self.UIClass_obj.white, self.UIClass_obj.start_font_style)

        # Display the timer in seconds while the game is being played
        announceObserver.observerDisplay('Time: {}'.format(self.elapsedTime), self.screen, [self.UIClass_obj.window_width // 2 + 60, 0], 18, self.UIClass_obj.white, self.UIClass_obj.start_font_style)

        announceObserver.observerDisplay('Lives: {}'.format(self.numLives), self.screen, [self.UIClass_obj.window_width // 4 + 60, 0], 18, self.UIClass_obj.white, self.UIClass_obj.start_font_style)

        # Draw the player
        self.player.drawPlayer()

        # Draw each enemy
        for x in self.enemy_list:
            x.draw()

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

            # TODO: Reset all of the enemy positions (Rohan)
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

    # If the game is over, we create a end game menu
    def endGameDraw(self):

        # Fill the entire window with a black background
        self.screen.fill(self.UIClass_obj.black)

        # Set the window dimensions
        window_width = self.UIClass_obj.window_width
        window_height = self.UIClass_obj.window_height

        # Create the announcing observer
        announceObserver = observerMethod()

        # Display the end game menu texts
        announceObserver.observerDisplay("GAME OVER", self.screen, [window_width // 2, window_height // 2 - 150],  52, self.UIClass_obj.red,  "arial", centered = True)
        announceObserver.observerDisplay("Play Again: SPACE", self.screen, [window_width // 2, window_height // 2 - 50],  36, (190, 190, 190), "arial", centered = True)
        announceObserver.observerDisplay("Quit Game: ESCAPE", self.screen, [window_width // 2, window_height // 2 - 10],  36, (190, 190, 190), "arial", centered = True)

        # Score text
        announceObserver.observerDisplay('Score: {}'.format(self.player.returnScore()), self.screen, [window_width // 2, window_height // 2 + 90],  36, (190, 190, 190), "arial", centered = True)

        # Timer text
        elapsedTime2 = str(self.elapsedTime)
        announceObserver.observerDisplay('Time: {} seconds'.format(elapsedTime2), self.screen, [window_width // 2, window_height // 2 + 130],  36, (190, 190, 190), "arial", centered = True)

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

        # TODO: Set the enemies back to the starting position (Rohan)
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
        with open("board_walls.txt", 'r') as file:
            #Traverse the file
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    #On a coin so add it
                    if char == 'C':
                        self.coins.append(vec(x, y))

        # Set the game state to playing
        self.state = GameState.PLAYING

########################################
# OBSERVER BELOW #
########################################

# This observer will help declare any text during the game such as: Score, Time, Lives, and menus.
class observerMethod():

    # Method that will be used declare any actions/changes that occur during the game.
    def observerDisplay(self, words, screen, pos, size, color, font_name, centered=False):

        # Set font, size, and color
        # The text needs to be centered or it will not show up on the pygame window
        if centered:
            pos[0] = pos[0] - pygame.font.SysFont(font_name, size).render(words, False, color).get_size()[0] // 2
            pos[1] = pos[1] - pygame.font.SysFont(font_name, size).render(words, False, color).get_size()[1] // 2

        screen.blit(pygame.font.SysFont(font_name, size).render(words, False, color), pos)

########################################
# DRIVER BELOW #
########################################

if __name__ == '__main__':
    pygame.init()
    Driver().runGame()
