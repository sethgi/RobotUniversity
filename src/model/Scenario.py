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
from utils import utils
import model.GamePiece as GamePiece
from model.Robot import Robot 
from model.Map import Map
from render.RenderGame import GameRenderer

import pygame

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

		# TODO: Break this out into some controller features
		self.checkboxes		= {}
		self.dropdowns		= {}
		
		self.taskStack		= []
		self.debugString	= []

		self.startTime		= None
		self.time					= None

		self.points				= 0

	def getMap(self) -> Map:
		return self.map

	def start(self) -> None:
		self.startTime = time.time()
		self.time			 = 0

if __name__ == "__main__":
	game = GameState("configs/scenarios/base.yaml")
	renderer = GameRenderer(1000,1000,game)
	
	pygame.init()
	
	# Set up the drawing window
	screen = pygame.display.set_mode([1000, 1000])

	# Run until the user asks to quit
	running = True
	while running:

			# Did the user click the window close button?
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
					running = False

		surf = pygame.transform.flip(renderer.render(), False, True)

		screen.blit(surf, (0,0))

		# Flip the display
		pygame.display.flip()

	pygame.quit()
