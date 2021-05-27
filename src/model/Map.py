import utils
import sympy.geometry as geometry
import yaml

# Base class for 'game piece', which is just some thing in the game
class Map:
	def __init__(self, path: str) -> None:
		mapConfig = yaml.load(open(path), Loader=yaml.FullLoader)

		self.width = utils.loadSafe(mapConfig, "width")
		self.height = utils.loadSafe(mapConfig, "height")

		w,h = self.width, self.height
		corners = ((0,0), (0,w), (h,0), (h,w))
		self.bounds = geometry.Polygon(*corners)

		obstacles = utils.loadListSafe(mapConfig, "obstacles", strict=False)
		self.obstacles = list(map(self.loadObstacle, obstacles))

		walls = utils.loadListSafe(mapConfig, "walls", strict=False)
		self.walls = list(map(self.loadWall, walls))
	
	def loadObstacle(self, obstacle):
		shape = utils.loadSafe(obstacle, "shape")

		if shape == "rectangle":
			width = utils.loadSafe(obstacle, "width")
			height = utils.loadSafe(obstacle, "height")
			xPosition = utils.loadSafe(obstacle, "xPosition")
			yPosition = utils.loadSafe(obstacle, "yPosition")
			rotation = utils.loadSafe(obstacle, "rotation", \
																	strict=False, default=0)

			return utils.makeBoundingBox(xPosition, yPosition, \
																width, height, rotation)	

		elif shape == "circle":
			xPosition = utils.loadSafe(obstacle, "xPosition")
			yPosition = utils.loadSafe(obstacle, "yPosition")
			radius = utils.loadSafe(obstacle, "radius")

			center = geometry.Point(xPosition, yPosition)
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
