"""
File: Scenario.py
Description: Model of the game state. 
Author: Seth Isaacson
"""

import time
import yaml
import pygame
import os
from pathlib import Path

from utils import utils
from model import GamePiece
from model.Robot import Robot 
from model.Map import Map
from render.GameRenderer import GameRenderer


# Store the current state of the execution
class GameState:	
	def __init__(self, config: str) -> None:
		fullPath = os.path.join(Path(__file__).parent, "../../", config)
		with open(fullPath) as f:
			game_config = yaml.load(f, Loader=yaml.FullLoader)

			robot_config = utils.loadSafe(game_config, "Robot")
			self._robot_state = Robot(robot_config)

			items = utils.loadSafe(game_config, "Items", strict=False)
			self._gripper_items = GamePiece.makePieceSet(items, GamePiece.GripperItem)

			torpedoTargets = utils.loadSafe(game_config, "TorpedoTargets", strict=False)
			self._torpedo_targets = GamePiece.makePieceSet(torpedoTargets, GamePiece.TorpedoTarget)
			
			dropLocations = utils.loadSafe(game_config, "DropLocations", strict=False)
			self._drop_locations = GamePiece.makePieceSet(dropLocations, GamePiece.DropLocation)
			
			map_path = utils.loadSafe(game_config, "Map")
			full_map_path = os.path.join(Path(__file__).parent, "../../", "configs", "maps", map_path)
			self._map = Map(full_map_path)

		# TODO: Break this out into some controller features
		self._checkboxes		= {}
		self._dropdowns		= {}
		 
		self._task_stack		= []
		self._debug_string	= []
     
		self._start_time		= None
		self._time					= None

		self._points				= 0

	def getMap(self) -> Map:
		return self._map

	def start(self) -> None:
		self._start_time = time.time()
		self._time			 = 0
