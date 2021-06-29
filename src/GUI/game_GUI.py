import pygame
from pygame.locals import *
import sys
import Scenario # how do i do this
sys.path.append('../')

# scenario, line 8-11 and 23
class gameGUI():
    def __init__(self):
        self.gameState = GameState("configs/scenarios/base.yaml")
        self.mapState = GameState("configs/maps/base.yaml")
        self._screenSize = (1000,600)

    def run(self):
        running = True
        pygame.init()
        screen = pygame.display.set_mode(self._screenSize)
        while(running):
            for event in pygame.event.get():
                # Handles quitting the game
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

if __name__ == '__main__':
    gui = gameGUI()
    gui.run()