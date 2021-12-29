import sys
import os.path
from pathlib import Path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import pygame

from utils.logger import *

class Renderer:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        
    def render(self):
        surf = self.doRender()

        width,height = surf.get_width(), surf.get_height()

        if (width,height) != (self._width, self._height):
            Warn(f"DoRender returned dimensions ({width},{height}),"
                 " but the renderer (type {self.__class__.__name__})"
                 " is configured to dimensions ({self._width}, {self._height})."
                 " Scaling appropriately.")
            surf = pygame.transform.Scale(self._width, self._height)

        return surf

    def doRender(self) -> pygame.Surface:
        raise Exception("Not Implemented")
