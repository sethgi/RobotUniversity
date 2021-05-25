import utils
from typing import List

class GamePiece:
	def __init__(self, name: str, id: int, config: dict) -> None:
		self.name = name
		self.id = id

		self.image = utils.loadImageSafe(config, "image")
		position = utils.loadListSafe(config, "position", 2)

		self.xPosition, self.yPosition = position

class GripperItem(GamePiece):
	pass

class TorpedoTarget(GamePiece):
	def __init__(self, name: str, id: int, config: dict) -> None:
		super().__init__(name, id, config)

		self.radius = utils.loadSafe(config, "radius", strict=False, default=1)
		self.blocked = utils.loadSafe(config, "radius", strict=False, default=False)

class DropLocation(GamePiece):
	def __init__(self, name: str, id: int, config: dict) -> None:
		super().__init__(name, id, config)

		outcomeBlock = utils.loadSafe(config, "outcome", strict=False)

		if outcomeBlock is None:
			target, action, reversible = None, None, None
		else:
			target = utils.loadSafe(outcomeBlock, "target")
			action = utils.loadSafe(outcomeBlock, "action")
			reversible = utils.loadSafe(outcomeBlock, "reversible", strict=False, default=False)


def makePieceSet(configs: List[dict], constructor: type):

		result = []
		if configs is None:
			return []
		
		elif type(configs) != list:
			raise Exception("You must supply a list of torpedo targets.")
		
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
