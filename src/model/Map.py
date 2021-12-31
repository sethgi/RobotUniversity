import sympy.geometry as geometry
import yaml

from utils import utils

# Base class for 'game piece', which is just some thing in the game
class Map:
	def __init__(self, path: str) -> None:
		map_config = yaml.load(open(path), Loader=yaml.FullLoader)

		self._width = utils.loadSafe(map_config, "width")
		self._height = utils.loadSafe(map_config, "height")

		w,h = self._width, self._height
		corners = ((0,0), (0,w), (h,0), (h,w))
		self._bounds = geometry.Polygon(*corners)

		obstacles = utils.loadListSafe(map_config, "obstacles", strict=False)
		self._obstacles = list(map(self.loadObstacle, obstacles))

		walls = utils.loadListSafe(map_config, "walls", strict=False)
		self._walls = list(map(self.loadWall, walls))
		
		self._wall_color = utils.loadSafe(map_config, "wall_color")
		self._obstacle_color = utils.loadSafe(map_config, "obstacle_color")

	def __eq__(self, other):
		return self._bounds == other._bounds and self._walls == other._walls and self._obstacles == other._obstacles

	def getWalls(self):
		return self._walls

	def getBounds(self):
		return self._bounds

	def getObstacles(self):
		return self._obstacles

	def getWidth(self):
		return self._width

	def getHeight(self):
		return self._height

	def loadObstacle(self, obstacle):
		shape = utils.loadSafe(obstacle, "shape")

		if shape == "rectangle":
			width = utils.loadSafe(obstacle, "width")
			height = utils.loadSafe(obstacle, "height")
			x_position, y_position = utils.loadListSafe(obstacle, "position")
			rotation = utils.loadSafe(obstacle, "rotation", \
																	strict=False, default=0)

			return utils.makeBoundingBox(x_position, y_position, \
																width, height, rotation)	

		elif shape == "circle":
			x_position, y_position = utils.loadListSafe(obstacle, "position")
			radius = utils.loadSafe(obstacle, "radius")

			center = geometry.Point(x_position, y_position)
			return geometry.Circle(center, radius)

		elif shape == "polygon":
			points = tuple(utils.loadSafe(obstacle, "corners"))
			return geometry.Polygon(*points)

		else:
			raise Exception("Shape {} unknown in map's obstacle list".format(shape))

	def loadWall(self, wall):
		start = utils.loadListSafe(wall, "start")
		end = utils.loadListSafe(wall, "end")

		return geometry.Line(geometry.Point(start), geometry.Point(end))
