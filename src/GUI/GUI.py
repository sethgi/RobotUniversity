import pygame
from pygame.locals import *
import sys
sys.path.append('../')

class simpleGUI():
    def __init__(self):
        self._gameScene = None
        self._controlScene = None
        self._gameStateScene = None
        self._visScene = None
        self._screenSize = (1500,800)

    def run(self):
        running = True
        pygame.init()
        screen = pygame.display.set_mode(self._screenSize, HWSURFACE | DOUBLEBUF | RESIZABLE)
        while(running):
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == VIDEORESIZE:
                    newSize = event.dict['size']
                    ### TODO: Handle Scene Resizing 
                    self._screenSize = newSize
                elif event.type == VIDEOEXPOSE:
                    newSize = screen.get_size()
                    ## TODO Handle Scene Resizing
                    self._screenSize = newSize
                    
if __name__ == '__main__':
    gui = simpleGUI()
    gui.run()
