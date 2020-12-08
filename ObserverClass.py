#Creates the Observer Design Pattern

########################################
# NOTES BELOW #
########################################

#In creation of this file, REFERENCED:
    #https://refactoring.guru/design-patterns/observer/python/example (Observer)

########################################
# IMPORTS BELOW #
########################################

#Import 3rd Party Libraries
import pygame

########################################
# OBSERVER BELOW #
########################################

#Notes:
    #This observer will help declare any text during the game such as: Score, Time, Lives, and menus.
class ObserverClass():

    #Static observer_list attribute; saves a list of all observers subscribed
    observer_list = []

    #Adds an observer to observer_list
    def registerObserver(self, obs):
        self.observer_list.append(obs)

    #Removes an observer from observer_list
    def unregisterObserver(self, obs):
        self.observer_list.remove(obs)

    # Method that will be used declare any actions/changes that occur during the game.
    def observerDisplay(self, words, screen, pos, size, color, font_name, centered=False):

        # Set font, size, and color
        # The text needs to be centered or it will not show up on the pygame window
        if centered:
            pos[0] = pos[0] - pygame.font.SysFont(font_name, size).render(words, False, color).get_size()[0] // 2
            pos[1] = pos[1] - pygame.font.SysFont(font_name, size).render(words, False, color).get_size()[1] // 2

        screen.blit(pygame.font.SysFont(font_name, size).render(words, False, color), pos)