import pygame
from constants import *
import random
vec = pygame.math.Vector2 
#enemy bit states 0 is fast pursuit, 1 is slow pursuit, 2 is targeted 3 is random
class Enemy:
    def __init__(self, app, pos, name, bit_state):
        self.app = app
        self.enemy_bit_state = bit_state
        self.name = name
        self.current_grid_pos = pos
        self.current_pix_pos = self.getPixPos();
        self.starting_pos = [pos.x, pos.y]
        #color attribute determined in the factory
        #self.id 
        self.direction = vec(0,0)
        self.player_target = None
        self.radii = int(self.app.cell_width//2.3)
        self.speed = self.getSpeed()
        #self.enemy_movement = self.getEnemyMovement()
        
    def getPixPos(self):
        x = (self.current_grid_pos.x*self.app.cell_width)+TOP_BOTTOM_MARGIN//2+self.app.cell_width//2
        y = (self.current_grid_pos.y*self.app.cell_height)+TOP_BOTTOM_MARGIN//2 + self.app.cell_height//2
        return vec(x,y)
                   
    def getSpeed(self):
        if self.enemy_bit_state != 1:
            self.speed = 2
        else:
            self.speed = 1
        return self.speed;
    '''
    def getEnemyMovement(self):
        if self.enemy_bit_state==0:
            return "fast_pursuit"
        elif(self.enemy_bit_state==1):
            return "slow_pursuit"
        else:
            return "targeted"
    '''
    def getTarget(self):
        if self.enemy_bit_state==0 or self.enemy_bit_state ==1:
            return self.app.player.current_grid_pos
        else:
            if self.app.player.current_grid_pos[0] > COLS//2 and self.app.player.current_grid_pos[1] > ROWS//2:
                vec(1,1)
            if self.app.player.current_grid_pos[0] > COLS//2 and self.app.player.current_grid_pos[1] < ROWS//2:
                return vec(1, ROWS-2)
            if self.app.player.current_grid_pos[0] < COLS//2 and self.app.player.current_grid_pos[1] > ROWS//2:
                return vec(COLS-2, 1)
            else:
                return vec(COLS-2, ROWS-2)

       
    def canMove(self):
        x = int(self.pix_pos.x+TOP_BOTTOM_MARGIN//2) % self.app.cell_width
        y = int(self.pix_pos.y+TOP_BOTTOM_MARGIN//2) % self.app.cell_height
        if  x == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if  y == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False
    def enemyMove(self):
        if(self.enemy_bit_state == 0 or self.enemy_bit_state==1 or self.enemy_bit_state==2):
            self.direction = self.findNextPos(self.player_target)
        if(self.enemy_bit_state==3):
            listChoice = [[1,0],[0,1],[-1,0],[0,-1]]
            randomChoice = random.sample(listChoice,4)
            self.direction = vec(randomChoice[0],randomChoice[1])

    def setCurrentPixPos(self):
        if self.player_target != self.current_grid_pos:
            self.current_pix_pos += self.direction * self.speed
            return True
    def findNextPos(self,player_target):
        vec_pos = self.BreadthFirstSearchEnemyTarget([int(self.current_grid_pos.x), int(self.current_grid_pos.y)], [int(player_target[0]), int(player_target[1])])[1]
        delta_x = vec_pos[0]-self.current_grid_pos[0] 
        delta_y = vec_pos[1]-self.current_grid_pos[1]
        return vec(delta_x,delta_y)
    def BreadthFirstSearchEnemyTarget(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest
    def pixPos_To_GridPos_X(self):
        self.current_grid_pos[0] = (self.current_pix_pos[0]-TOP_BOTTOM_MARGIN + self.app.cell_width//2)//self.app.cell_width+1

    def pixPos_To_GridPos_Y(self):
        self.current_grid_pos[1] = (self.current_pix_pos[1]-TOP_BOTTOM_MARGIN + self.app.cell_height//2)//self.app.cell_height+1

    def updateEnemyState(self):
        self.player_target = self.getTarget()
        if self.setCurrentPixPos() == True:
            if self.canMove == True:
                self.enemyMove()
        self.pixPos_To_GridPos_X()
        self.pixPos_To_GridPos_Y()
class BlueEnemy(Enemy):
    def draw(self):
        pygame.draw.circle(self.app.screen, (0, 255, 255), (int(self.current_pix_pos.x), int(self.current_pix_pos.y)), self.radii)

class OrangeEnemy(Enemy):
    def draw(self):
        pygame.draw.circle(self.app.screen, (255, 184, 82), (int(self.current_pix_pos.x), int(self.current_pix_pos.y)), self.radii)

class RedEmemy(Enemy):
    def draw(self):
        pygame.draw.circle(self.app.screen, (255, 0, 0), (int(self.current_pix_pos.x), int(self.current_pix_pos.y)), self.radii)


class PinkEmemy(Enemy):
    def draw(self):
        pygame.draw.circle(self.app.screen, (255, 184, 255), (int(self.current_pix_pos.x), int(self.current_pix_pos.y)), self.radii)


class EnemyFactory():
    def CreateEnemy(self, type, app, pos, name, bit_state):
        if(type == "Blue"):
            return BlueEnemy(app, pos, name, bit_state)
        elif(type=="Orange"):
            return OrangeEnemy(app, pos, name, bit_state)
        elif(type=="Red"):
            return RedEmemy(app, pos, name, bit_state)
        elif(type=="Pink"):
            return PinkEmemy(app, pos, name, bit_state)
        #return None

if __name__ == '__main__':
    #instance = Enemy()
    listChoice = [[1,0],[0,1],[-1,0],[0,-1]]
    randomChoice = random.sample(listChoice,4)
    print(vec(randomChoice[0],randomChoice[1]))