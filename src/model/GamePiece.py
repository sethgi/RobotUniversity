from typing import List
import sympy.geometry as geometry

from utils import utils

# Base class for 'game piece', which is just some thing in the game
class GamePiece:
	def __init__(self, name: str, id: int, config: dict) -> None:
		self._name = name
		self._id = id

		self._image = utils.loadImageSafe(config, "image")
		position = utils.loadListSafe(config, "position", 2)

		self._position = geometry.Point(position)
		self._theta = utils.loadSafe(config, "theta", strict=False, default=0, warnIfMissing=False)

		self._width = utils.loadSafe(config, "width", strict=False, default=0.01, warnIfMissing=False)
		self._height = utils.loadSafe(config, "height", strict=False, default=0.01, warnIfMissing=False)

		x,y = position
		self._bounding_box = utils.makeBoundingBox(x,y,self._width, self._height, self._theta)

# GripperItem is an item that the gripper can use
class GripperItem(GamePiece):
	pass

# Locations of targets for torpedos
class TorpedoTarget(GamePiece):
	def __init__(self, name: str, id: int, config: dict) -> None:
		super().__init__(name, id, config)

		self._radius = utils.loadSafe(config, "radius", strict=False, default=1)
		self._blocked = utils.loadSafe(config, "radius", strict=False, default=False)

# Locations to drop off gripper items
class DropLocation(GamePiece):
	def __init__(self, name: str, id: int, config: dict) -> None:
		super().__init__(name, id, config)

		# Which item it expects. If None, it accepts any GripperItem
		self._received_item = utils.loadSafe(config, "receives", strict=False)

		outcomeBlock = utils.loadSafe(config, "outcome", strict=False)

		if outcomeBlock is None:
			target, action, reversible = None, None, None
		else:
			self._target = utils.loadSafe(outcomeBlock, "target")
			self._action = utils.loadSafe(outcomeBlock, "action")
			self._reversible = utils.loadSafe(outcomeBlock, "reversible", strict=False, default=False)

# Configure a set of pieces of a single type from a block in yaml.
# The input type is some class which inherits from GamePiece
def makePieceSet(configs: List[dict], constructor: type) -> List:

		result = []
		if configs is None:
			return []
		
		elif type(configs) != list:
			raise Exception("You must supply a list of items.")
		
		else:
			for config, id in zip(configs, range(len(configs))):
				keys = list(config.keys())
				if len(keys) != 1:
					raise Exception(f"The configuration for the list of {constructor.__name__}"
									 "does not  follow the required form."\
									 " Make sure it matches the template")

				name = list(config.keys())[0]
				result.append(constructor(name, id, config[name]))
				
			return result
