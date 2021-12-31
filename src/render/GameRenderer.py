import pygame
import sympy.geometry as geometry

from model.Map import Map
from render.Widget import Widget

# TODO: Don't hardcode colors etc.
# TODO: getters in maps
    
class GameRenderer(Widget):
    def __init__(self, width: int, height: int, game_state: "GameState") -> None:
        super().__init__(width, height)
        self._game_state = game_state

        self._background_color = (255,255,255)
        self._obstacle_color = (255,0,0)
        self._wall_color = (0,0,255)
        self._wall_width = 5

    def doRender(self) -> pygame.Surface:
        surf = pygame.Surface((self._width, self._height))
        surf.fill(self._background_color)

        game_map = self._game_state.getMap()
        self.renderMap(game_map, surf)

        return surf

    def renderMap(self, game_map: Map, surf: pygame.Surface) -> None:
        width_to_px = self._width / game_map.getWidth()
        height_to_px = self._height / game_map.getHeight()

        for wall in game_map.getWalls():
            x_start, y_start = wall.p1
            x_end, y_end = wall.p2
            
            start_pos = (int(x_start * width_to_px),
                         int(y_start * height_to_px))

            end_pos = (int(x_end * width_to_px),
                       int(y_end * height_to_px))
            pygame.draw.line(surf, self._wall_color,
                             start_pos, end_pos,
                             width=self._wall_width)
      
        for obstacle in game_map.getObstacles():
            if isinstance(obstacle, geometry.Polygon):
                vertices = [(int(x * width_to_px), int(y * height_to_px)) for x,y in obstacle.vertices]
                pygame.draw.polygon(surf, self._wall_color, vertices)
            elif isinstance(obstacle, geometry.Circle):
                center = (int(obstacle.center[0] * width_to_px), int(obstacle.center[1] * height_to_px))
                hradius = obstacle.hradius * width_to_px
                vradius = obstacle.vradius * height_to_px

                bounding_rect = (int(center[0]-hradius), int(center[1]-vradius), int(hradius*2), int(vradius*2))
                pygame.draw.ellipse(surf, self._wall_color, bounding_rect)
            else:
                raise Exception(f"Obstacle has invalid type {obstacle.__class__.__name__}")

    
