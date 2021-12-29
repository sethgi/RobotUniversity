from utils import utils
from typing import List
import sympy.geometry as geometry

# Base class for 'game piece', which is just some thing in the game
class GamePiece:
	def __init__(self, name: str, id: int, config: dict) -> None:
		self.name = name
		self.id = id

		self.image = utils.loadImageSafe(config, "image")
		position = utils.loadListSafe(config, "position", 2)

		self.position = geometry.Point(position)
		self.theta = utils.loadSafe(config, "theta", strict=False, default=0, warnIfMissing=False)

		self.width = utils.loadSafe(config, "width", strict=False, default=0.01, warnIfMissing=False)
		self.height = utils.loadSafe(config, "height", strict=False, default=0.01, warnIfMissing=False)

		x,y = position
		self.boundingBox = utils.makeBoundingBox(x,y,self.width,self.height, self.theta)

# GripperItem is an item that the gripper can use
class GripperItem(GamePiece):
	pass

# Locations of targets for torpedos
class TorpedoTarget(GamePiece):
	def __init__(self, name: str, id: int, config: dict) -> None:
		super().__init__(name, id, config)

		self.radius = utils.loadSafe(config, "radius", strict=False, default=1)
		self.blocked = utils.loadSafe(config, "radius", strict=False, default=False)

# Locations to drop off gripper items
class DropLocation(GamePiece):
	def __init__(self, name: str, id: int, config: dict) -> None:
		super().__init__(name, id, config)

		# Which item it expects. If None, it accepts any GripperItem
		self.receivedItem = utils.loadSafe(config, "receives", strict=False)

		outcomeBlock = utils.loadSafe(config, "outcome", strict=False)

		if outcomeBlock is None:
			target, action, reversible = None, None, None
		else:
			self.target = utils.loadSafe(outcomeBlock, "target")
			self.action = utils.loadSafe(outcomeBlock, "action")
			self.reversible = utils.loadSafe(outcomeBlock, "reversible", strict=False, default=False)

# Configure a set of pieces of a single type from a block in yaml.
# The input type is some class which inherits from GamePiece
def makePieceSet(configs: List[dict], constructor: type):

		result = []
		if configs is None:
			return []
		
		elif type(configs) != list:
			raise Exception("You must supply a list of items.")
		
		else:
			for config, id in zip(configs, range(len(configs))):
				keys = list(config.keys())
				if len(keys) != 1:
					# TODO: Make "items" tell the actual type of the issue
					raise Exception("The items list does not follow the required form."\
									 " Make sure it matches the template")

				name = list(config.keys())[0]
				result.append(constructor(name, id, config[name]))
				
			return result
