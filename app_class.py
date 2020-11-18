import pygame

import sys
from PlayerClass import *
from enemy_class import *


pygame.init()
vec = pygame.math.Vector2

# Create the application class
class App:

    # Initialize variables
    def __init__(self):

        # Create the board to be played on
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Create the timer that will keep running during the game
        self.timer = pygame.time.Clock()

        # Set the running state to True
        self.running = True

        # Set the start state to 'start'
        self.state = 'start'

        # Set the size of the cell based on the constants file
        self.cell_width = BOARD_WIDTH//COLS
        self.cell_height = BOARD_HEIGHT//ROWS

        # Create the arrays for the walls, coins, enemies, and enemy positions to fill and update over time
        self.walls = []
        self.coins = []
        self.enemies = []
        self.enemy_positions = []

        # Create the player's position to start and where it will be updated over time
        self.player_position = None

        # Load the image of the board and the scale the game to it's size
        self.load()

        # Create our new player
        self.player = SingletonPlayer.getInstance(self, vec(self.player_position))

        # Populate our enemies array by creating enemies
        self.create_enemies()

    # Begin running the program
    def run(self):

        # While the game is running
        while self.running:

            # If it is the start of the game
            if self.state == 'start':

                # Run the events class which corresponds to starting the program
                self.program_start()
                self.program_update()
                self.program_draw()

            # If it is currently during the game
            elif self.state == 'playing':

                # Run the events class which corresponds to currently running the program
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            # If it is the end of the game
            elif self.state == 'game over':

                # Run the events class which corresponds to ending the program
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()

            # If none, the program should no longer be running
            else:
                self.running = False

            # Increment the timer
            self.timer.tick(FPS)

        # Once everything is done quit the game
        pygame.quit()
        sys.exit()

    # Load in the board image, and the grid that overlaps the board within the pygame window
    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (BOARD_WIDTH, BOARD_HEIGHT))

        # Create the playable board using the walls.txt file
        with open("walls.txt", 'r') as file:

            # For each line in the file, we need to go through and see what each item is
            for y, line in enumerate(file):

                # Check what the item is
                for x, char in enumerate(line):

                    # If the value is a 1, it's a wall
                    if char == "1":
                        self.walls.append(vec(x, y))

                    # If the value is a C, it's a coin
                    elif char == "C":
                        self.coins.append(vec(x, y))

                    # If the value is a P, it's a player
                    elif char == "P":
                        self.player_position = [x, y]

                    # If the value is 2, 3, 4, or 5, it's an enemy
                    elif char in ["2", "3", "4", "5"]:
                        self.enemy_positions.append([x, y])

                    # If the value is a B, then it's the background
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (x*self.cell_width, y*self.cell_height, self.cell_width, self.cell_height))

    # Draw the coins as a circle
    def draw_coins(self):

        # For each coin, draw the coin
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 10), (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_MARGIN // 2, int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_MARGIN // 2), 5)


    # We create enemies using a enemy factory from the enemy class
    def create_enemies(self):

        # Create an enemy factory object
        theFactory = EnemyFactory()

        # def CreateEnemy(self, type, app, pos, name, bit_state):
        for x, pos in enumerate(self.enemy_positions):

            # Create a Blue Enemy
            # x will also be used to set the behavior bit for each enemy
            if x == 0:
                self.enemies.append(theFactory.CreateEnemy("Blue", self, vec(pos), BlueEnemy, x))

            # Create a Orange Enemy
            elif x == 1:
                self.enemies.append(theFactory.CreateEnemy("Orange", self, vec(pos), OrangeEnemy, x))

            # Create a Red Enemy (note enemy spelled incorrectly)
            elif x == 2:
                self.enemies.append(theFactory.CreateEnemy("Red", self, vec(pos), RedEmemy, x))

            # Create a Pink Enemy (note enemy spelled incorrectly)
            elif x == 3:
                self.enemies.append(theFactory.CreateEnemy("Pink", self, vec(pos), PinkEmemy, x))

    # Make a way for text to be displayed during the game
    def display_text(self, words, screen, pos, size, color, font_name, centered = False):

        # Set font, size, and color
        # The text needs to be centered or it will not show up on the pygame window
        if centered:

            pos[0] = pos[0]-pygame.font.SysFont(font_name, size).render(words, False, color).get_size()[0]//2
            pos[1] = pos[1]-pygame.font.SysFont(font_name, size).render(words, False, color).get_size()[1]//2

        screen.blit(pygame.font.SysFont(font_name, size).render(words, False, color), pos)

    # Program start event
    def program_start(self):

        for event in pygame.event.get():

            # If the game is quit, set the running state to False
            if event.type == pygame.QUIT:
                self.running = False

            # If the user inputs a key, start the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    # We don't need to really update anything if the program has just started
    def program_update(self):
        pass

    # Draw the board
    def program_draw(self):

        self.screen.fill(BLACK)

        # Tell the player what button to push to start playing
        self.display_text('PUSH SPACE BAR', self.screen, [WINDOW_WIDTH//2, WINDOW_HEIGHT//2-50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered = True)

        # Tell the player that there will only be one player at once
        self.display_text('1 PLAYER ONLY', self.screen, [WINDOW_WIDTH//2, WINDOW_HEIGHT//2+50], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered = True)

        # Update the display
        pygame.display.update()

    # Currently playing event
    def playing_events(self):

        # For each event that occurs during the game
        for event in pygame.event.get():

            # If the event is to quit the game, set the running state to False
            if event.type == pygame.QUIT:
                self.running = False

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

    # Update while playing
    def playing_update(self):

        # Update the player's state
        self.player.updatePlayerState()

        # Update each enemy's state
        for enemy in self.enemies:
            enemy.updateEnemyState()

        # If the player and an enemy are in the same place, that means the player has died
        for enemy in self.enemies:

            if enemy.getPixPos() == self.player.getPixPos():

                # Remove a life since the player has died
                self.remove_life()

    # Draw the board during the game
    def playing_draw(self):

        self.screen.fill(BLACK)

        self.screen.blit(self.background, (TOP_BOTTOM_MARGIN//2, TOP_BOTTOM_MARGIN//2))

        # Draw the coins
        self.draw_coins()

        # Display the current score         THIS SHOULD BE AN OBSERVER METHOD LATER ON
        self.display_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [60, 0], 18, WHITE, START_FONT)

        # Display the timer NOT WORKING RIGHT NOW       THIS SHOULD BE AN OBSERVER METHOD LATER ON
        self.display_text('Timer: '.format(self.timer), self.screen, [WINDOW_WIDTH//2+60, 0], 18, WHITE, START_FONT)

        # Draw the player
        self.player.drawPlayer()

        # Draw each enemy
        for enemy in self.enemies:
            enemy.draw()

        # Display the update
        pygame.display.update()

    # Function for when a player loses a life
    def remove_life(self):

        # Reduce the lives count by 1
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

            # Reset all of the enemy positions
            for enemy in self.enemies:

                # Set the grid position of the enemy to the starting position
                enemy.grid_pos = vec(enemy.starting_pos)

                # Set the pixel position of the of the enemy to the starting position
                enemy.pix_pos = enemy.getPixPos()

                # Set the direction of the player to no direction
                enemy.direction *= 0

    # Event for when the game is over
    def game_over_events(self):

        for event in pygame.event.get():

            # If the user quits the game set the running state to False
            if event.type == pygame.QUIT:
                self.running = False

            # If the player presses space in the end game menu, reset the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

            # If the player preses escape in the end game menu, exit out of the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    # We don't need to really update anything if the program has just started
    def game_over_update(self):
        pass

    # If the game is over, we create a end game menu
    def game_over_draw(self):

        self.screen.fill(BLACK)

        # Texts for the end game menu
        exitgamest = "Press ESCAPE to quit the game."
        replayt = "Press SPACE to play again."

        # Display the end game menu texts
        self.display_text("GAME OVER", self.screen, [WINDOW_WIDTH//2, 100],  52, RED, "arial", centered = True)
        self.display_text(replayt, self.screen, [WINDOW_WIDTH//2, WINDOW_HEIGHT//2],  36, (190, 190, 190), "arial", centered = True)
        self.display_text(exitgamest, self.screen, [WINDOW_WIDTH//2, WINDOW_HEIGHT//1.5],  36, (190, 190, 190), "arial", centered = True)

        # Timer text NOT WORKING RIGHT NOW          THIS SHOULD BE AN OBSERVER METHOD LATER ON
        # self.display_text(self.timer.tick(), self.screen, [WINDOW_WIDTH//2, WINDOW_HEIGHT//1],  36, (190, 190, 190), "arial", centered = True)

        # Update the display
        pygame.display.update()

    # Reset the game when appropriate
    def reset(self):

        # Set the lives back to 3
        self.player.lives = 3

        # Set the score back to 0
        self.player.current_score = 0

        # Set the player back to the starting location
        self.player.grid_pos = vec(self.player.starting_pos)

        # Set the player's pixel position back to the starting location
        self.player.pix_pos = self.player.getPixPos()

        # Set the character's moving/facing direction to nothing
        self.player.direction *= 0

        # Set the enemies back to the starting position
        for x in self.enemies:

            # Set the enemy's back to the starting location
            x.grid_pos = vec(x.starting_pos)

            # Set the enemy's pixel position back to the starting position
            x.pix_pos = x.getPixPos()

            # Set the enemy's moving/facing direction to nothing
            x.direction *= 0

        # Set the coins array back to empty
        self.coins = []

        # Reset the coin locations using the text file
        with open("walls.txt", 'r') as file:

            for y, line in enumerate(file):

                for x, char in enumerate(line):

                    if char == 'C':

                        self.coins.append(vec(x, y))

        self.state = "playing"