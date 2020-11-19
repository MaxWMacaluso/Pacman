import sys
import pygame

from PlayerClass import *
from EnemyClass import *
from UIClass import * 


# Create the Driver class
class Driver:

    # Constructor
    def __init__(self):
        #Make a new instance of UIClass
        self.UIClass_obj = UIClass()
        
        # Create the board to be played on
        self.screen = self.UIClass_obj.setMode()

        # Create the timer that will keep running during the game
        self.timer = self.UIClass_obj.gameClock()

        # Set the playing state to True
        self.playing = True

        # Set the start state to 'start'
        self.state = 'start'

        # Set the size of the cell based on the UIClass.py file
        self.cell_width = self.UIClass_obj.board_width // self.UIClass_obj.columns
        self.cell_height = self.UIClass_obj.board_height // self.UIClass_obj.rows

        # Create the lists for the walls, coins, enemies, and enemy positions to fill and update over time
        self.walls = []
        self.enemy_list = []
        self.enemy_positions = []
        self.coins = []

        # Create the player's position to start and where it will be updated over time
        self.player_position = None

        # Set the image of the board and the scale the game to it's size
        self.setgame()

        # Create our new player
        self.player = SingletonPlayer.getInstance(self, vec(self.player_position))

        # Populate our enemies array by creating enemies
        self.populateEnemies()

    # Begin running the game
    def game(self):

        # While the game is being played
        while self.playing:

            # If it is the start of the game
            if self.state == 'start':

                # Run the events class which corresponds to starting the program
                self.programStart()
                self.programDraw()

            # If it is currently during the game
            elif self.state == 'playing':

                # Run the classes which corresponds to currently playing the game
                self.currentlyPlaying()
                self.currentUpdates()
                self.currentDrawing()

            # TODO: If it is the end of the game

            # Increment the timer
            self.timer.tick(self.UIClass_obj.fps)

        # Once everything is done quit the game
        self.UIClass_obj.quitGame()
        sys.exit()

    # Set the board image, and the grid that overlaps the board within the pygame window
    def setgame(self):
        board_width = self.UIClass_obj.board_width
        board_height = self.UIClass_obj.board_height
        self.background = self.UIClass_obj.loadImg('bg.png')
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

                    # TODO: If the value is a C, it's a coin

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

    #   TODO: Draw the coins as a circle

    # We create enemies using a enemy factory from the enemy class
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

    # Make a way for text to be displayed during the game
    def displayStats(self, words, screen, pos, size, color, font_name, centered=False):

        # Set font, size, and color
        # The text needs to be centered or it will not show up on the pygame window
        if centered:
            pos[0] = pos[0] - pygame.font.SysFont(font_name, size).render(words, False, color).get_size()[0] // 2
            pos[1] = pos[1] - pygame.font.SysFont(font_name, size).render(words, False, color).get_size()[1] // 2

        screen.blit(pygame.font.SysFont(font_name, size).render(words, False, color), pos)

    # Program start event
    def programStart(self):

        for event in pygame.event.get():

            # If the game is quit, set the playing state to False
            if event.type == pygame.QUIT:
                self.playing = False

            # If the user inputs a key, start the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    # Draw the board
    def programDraw(self):

        self.screen.fill(self.UIClass_obj.black)
        window_width = self.UIClass_obj.window_width
        window_height = self.UIClass_obj.window_height
        font_style = self.UIClass_obj.start_font_style
        text_size = self.UIClass_obj.start_screen_text_size

        # Tell the player what button to push to start playing
        self.displayStats('Press SPACE to start', self.screen, [window_width // 2, window_height // 2 - 50], text_size, (170, 132, 58), font_style, centered=True)

        # Display Our Team Info
        self.displayStats('Pac Man Recreation', self.screen, [window_width // 2, window_height // 2 + 50], text_size, (44, 167, 198), font_style, centered=True)
        self.displayStats('Max Macaluso, Rohan Suri, Sahib Bajwa', self.screen, [window_width // 2, window_height // 2 + 100], text_size, (44, 167, 198), font_style, centered=True)

        # Update the display
        self.UIClass_obj.updateDisplay()

    # TODO: Currently playing event (MOVEMENT)
    def currentlyPlaying(self):

        # For each event that occurs during the game
        for event in pygame.event.get():

            # If the event is to quit the game, set the playing state to False
            if event.type == pygame.QUIT:
                self.playing = False

            # TODO: If the event is a keystroke

    # Update while playing
    def currentUpdates(self):

        # Update the player's state
        self.player.updatePlayerState()

        # Update each enemy's state
        for x in self.enemy_list:
            x.updateEnemyState()

        # If the player and an enemy are in the same place, that means the player has died
        for x in self.enemy_list:

            if x.getPixPos() == self.player.getPixPos():
                # Remove a life since the player has died
                self.decrementLives()

    # Draw the board during the game
    def currentDrawing(self):

        self.screen.fill(self.UIClass_obj.black)

        self.screen.blit(self.background, (self.UIClass_obj.vertical_margin // 2, self.UIClass_obj.vertical_margin // 2))

        # TODO: Draw the coins

        # Display the score         THIS SHOULD BE AN OBSERVER METHOD LATER ON
        self.displayStats('SCORE: {}'.format(self.player.current_score), self.screen, [60, 0], 18, self.UIClass_obj.white, self.UIClass_obj.start_font_style)

        # Display the timer in seconds NOT WORKING RIGHT NOW       THIS SHOULD BE AN OBSERVER METHOD LATER ON
        self.displayStats('Timer: {}'.format(self.timer), self.screen, [self.UIClass_obj.window_width // 2 + 60, 0], 18, self.UIClass_obj.white, self.UIClass_obj.start_font_style)

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
        self.player.num_lives -= 1

        # If the player has no lives, set the game state to over
        if self.player.num_lives == 0:
            self.state = "game over"

        # If the player still has lives
        else:

            # Set the grid position of the player as the starting position
            self.player.grid_pos = vec(self.player.starting_pos)

            # Set the pixel position of the player as the starting position
            self.player.pix_pos = self.player.getPixPos()

            # Set the direction of the player to no direction
            self.player.direction *= 0

            # TODO: Reset all of the enemy positions

    # TODO: Event for when the game is over

    # TODO: Reset the game when appropriate


    ########################################
    # DRIVER BELOW #
    ########################################

if __name__ == '__main__':
    pygame.init()
    Driver().game()
