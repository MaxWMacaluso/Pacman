#Utilizes the Simple Factory Design Pattern found in EnemyFactory.py

########################################
# NOTES BELOW #
########################################

#In creation of this file, REFERENCED:
    #https://pypi.org/project/pathfinding/ (Path-finding)
    #http://www.grantjenks.com/docs/freegames/pacman.html (referenced code)

########################################
# IMPORTS BELOW #
########################################

#Import 3rd Party Libraries
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

#Import all from UIClass
from UIClass import *

########################################
# ENEMY CLASS BELOW #
########################################

#Notes: 
    #Enemy bit states 0 is fast pursuit, 1 is slow pursuit, 2 is targeted 3 is random
class Enemy:
    def __init__(self, driver, pos, name, bit_state):
        self.UIClass_obj = UIClass() #Make a new instance of UIClass
        self.driver = driver
        self.enemy_bit_state = bit_state
        self.name = name
        self.current_grid_pos = pos
        self.current_pix_pos = self.getPixPos()
        self.starting_pos = [pos.x, pos.y]
        self.direction = vec(0,0)
        self.player_target = None
        self.radii = int(self.driver.cell_width // 2.3)
        self.speed = self.getSpeed()
        
    #Given the current grid position, calculate the pixel position
    def getPixPos(self):
        x = (self.current_grid_pos.x * self.driver.cell_width) + self.UIClass_obj.margin // 2 + self.driver.cell_width // 2
        y = (self.current_grid_pos.y * self.driver.cell_height) + self.UIClass_obj.margin // 2 + self.driver.cell_height // 2
        return vec(x,y)

    #Primary Path-finding algorithm in use
        #Utilizes A* Pathfinding Algorithm 
        #Returns a path to follow
    def AStarSearchEnemyTarget(self, start, target):
        board = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0],
        [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0],
        [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0],
        [0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0],
        [0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,1,0,5,1,1,1,1,4,0,1,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,1,0,2,1,1,1,1,3,0,1,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0],
        [0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0],
        [0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0],
        [0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0],
        [0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0],
        [0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        #board = [[0 for x in range(28)] for x in range(30)]
        grid = Grid(matrix = board)
        begin = grid.node(start[0], start[1])
        end = grid.node(target[0], target[1])
        finder = AStarFinder(diagonal_movement = DiagonalMovement.never)
        path, runs = finder.find_path(begin, end, grid)
        #print('operations:', runs, 'path length:', len(path))
        #print(path)
        return path

    def findNextPos(self, player_target):
        vec_pos = self.AStarSearchEnemyTarget([int(self.current_grid_pos.x), int(self.current_grid_pos.y)], [int(player_target[0]), int(player_target[1])])[1]
        delta_x = vec_pos[0]-self.current_grid_pos[0] 
        delta_y = vec_pos[1]-self.current_grid_pos[1]
        return vec(delta_x, delta_y)

    #Helper method to return the speed depending on the bit_state        
    def getSpeed(self):
        if self.enemy_bit_state != 1:
            self.speed = 2
        else:
            self.speed = 1
        return self.speed

    def getTarget(self):
        #Set these values to condense code
        rows = self.UIClass_obj.rows
        cols = self.UIClass_obj.columns
        up_x = (self.driver.player.current_grid_pos[0] > cols // 2)
        up_y = (self.driver.player.current_grid_pos[1] > rows // 2)
        down_x = (self.driver.player.current_grid_pos[0] < cols // 2)
        down_y = (self.driver.player.current_grid_pos[1] < rows // 2)

        if self.enemy_bit_state == 0:
            return self.driver.player.current_grid_pos
        elif self.enemy_bit_state == 1:
            return self.driver.player.current_grid_pos
        else:
            if up_x and up_y:
                return vec(1, 1)
            if up_x and down_y:
                return vec(1, rows - 2)
            if down_x and up_y:
                return vec(cols - 2, 1)
            else:
                return vec(cols - 2, rows - 2)

    
    def canMove(self):
        #Set x, y to condense code
        x = int(self.current_pix_pos.x + self.UIClass_obj.margin // 2) % self.driver.cell_width
        y = int(self.current_pix_pos.y + self.UIClass_obj.margin // 2) % self.driver.cell_height

        #To condense code
        right = (self.direction == vec(1, 0))
        left = (self.direction == vec(-1, 0))
        none = (self.direction == vec(0, 0))
        down = (self.direction == vec(0, 1))
        up = (self.direction == vec(0, -1))
        
        if  x == 0:
            if right or left or none:
                return True
        if  y == 0:
            if down or up or none:
                return True
        #All other cases, return false
        return False

    def enemyMove(self):
        if (self.enemy_bit_state == 0 or self.enemy_bit_state == 1 or self.enemy_bit_state == 2):
            self.direction = self.findNextPos(self.player_target)
        if (self.enemy_bit_state == 3):
            while True:
                listChoice = [[1, 0], [0, 1], [-1, 0], [0, -1]]
                randomChoice = random.choice(listChoice)
                #print(randomChoice[0],randomChoice[1])
                random_step = vec(self.current_grid_pos.x+randomChoice[0],self.current_grid_pos.y+randomChoice[1])
                if(random_step not in self.driver.walls):
                    break
            self.direction = vec(randomChoice[0], randomChoice[1])
            #self.direction = vec(0,0)

    def setCurrentPixPos(self):
        if self.player_target != self.current_grid_pos:
            self.current_pix_pos += self.direction * self.speed
            return True

    def pixPos_To_GridPos_X(self):
        self.current_grid_pos[0] = (self.current_pix_pos[0] - self.UIClass_obj.margin + self.driver.cell_width // 2) // self.driver.cell_width + 1

    def pixPos_To_GridPos_Y(self):
        self.current_grid_pos[1] = (self.current_pix_pos[1] - self.UIClass_obj.margin + self.driver.cell_height // 2) // self.driver.cell_height + 1

    def updateEnemyState(self):
        #Get the target
        self.player_target = self.getTarget()
        #If pre-conditions are correct...
        if self.player_target != self.current_grid_pos:
            self.current_pix_pos += self.direction * self.speed
            
            #If can move then do move
            if self.canMove():
                self.enemyMove()
        #Get current x, y grid position
        self.pixPos_To_GridPos_X()
        self.pixPos_To_GridPos_Y()