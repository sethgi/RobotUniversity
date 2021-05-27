"""
File: Scenario.py
Description: Model of the game state. 
Author: Seth Isaacson
"""

import sys
import os.path
from pathlib import Path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import time
import yaml
import utils
import GamePiece
from Robot import Robot 
from Map import Map

# Store the current state of the execution
class GameState:	
	def __init__(self, config: str) -> None:
		fullPath = os.path.join(Path(__file__).parent, "../../", config)
		with open(fullPath) as f:
			gameConfig = yaml.load(f, Loader=yaml.FullLoader)

			robotConfig = utils.loadSafe(gameConfig, "Robot")
			self.robotState = Robot(robotConfig)

			items = utils.loadSafe(gameConfig, "Items", strict=False)
			self.gripperItems = GamePiece.makePieceSet(items, GamePiece.GripperItem)

			torpedoTargets = utils.loadSafe(gameConfig, "TorpedoTargets", strict=False)
			self.torpedoTargets = GamePiece.makePieceSet(torpedoTargets, GamePiece.TorpedoTarget)
			
			dropLocations = utils.loadSafe(gameConfig, "DropLocations", strict=False)
			self.dropLocations = GamePiece.makePieceSet(dropLocations, GamePiece.DropLocation)
			
			mapPath = utils.loadSafe(gameConfig, "Map")
			fullMapPath = os.path.join(Path(__file__).parent, "../../", "configs", "maps", mapPath)
			self.map = Map(fullMapPath)

		self.checkboxes		= {}
		self.dropdowns		= {}
		
		self.taskStack		= []
		self.debugString	= []

		self.startTime		= None
		self.time					= None

		self.points				= 0


	def start(self) -> None:
		self.startTime = time.time()
		self.time			 = 0

if __name__ == "__main__":
	game = GameState("configs/scenarios/base.yaml")

