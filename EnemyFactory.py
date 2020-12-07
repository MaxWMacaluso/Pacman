#Creates Simple Factory Design Pattern

########################################
# NOTES BELOW #
########################################

#In creation of this file, REFERENCED:
    #https://www.geeksforgeeks.org/factory-method-python-design-patterns/ (factory)

########################################
# IMPORTS BELOW #
########################################

#Import all from UIClass and EnemyClass
from UIClass import *
from EnemyClass import *


########################################
# SIMPLE FACTORY BELOW #
########################################

class BlueEnemy(Enemy):
    def draw(self):
        self.UIClass_obj.drawCircle(self.driver.screen, self.UIClass_obj.blue, (int(self.current_pix_pos.x), int(self.current_pix_pos.y)), self.radii)

class OrangeEnemy(Enemy):
    def draw(self):
        self.UIClass_obj.drawCircle(self.driver.screen, self.UIClass_obj.orange, (int(self.current_pix_pos.x), int(self.current_pix_pos.y)), self.radii)

class RedEnemy(Enemy):
    def draw(self):
        self.UIClass_obj.drawCircle(self.driver.screen, self.UIClass_obj.red, (int(self.current_pix_pos.x), int(self.current_pix_pos.y)), self.radii)


class PinkEmemy(Enemy):
    def draw(self):
        self.UIClass_obj.drawCircle(self.driver.screen, self.UIClass_obj.pink, (int(self.current_pix_pos.x), int(self.current_pix_pos.y)), self.radii)

class EnemyFactory():
    def CreateEnemy(self, type, driver, pos, name, bit_state):
        if (type == "Blue"):
            return BlueEnemy(driver, pos, name, bit_state)
        elif (type == "Orange"):
            return OrangeEnemy(driver, pos, name, bit_state)
        elif (type == "Red"):
            return RedEnemy(driver, pos, name, bit_state)
        elif (type == "Pink"):
            return PinkEmemy(driver, pos, name, bit_state)
        #return None