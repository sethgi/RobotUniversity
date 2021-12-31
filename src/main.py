import pygame

import model.GamePiece
from model.Scenario import GameState
from render.GameRenderer import GameRenderer

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
	t = model.GamePiece.TorpedoTarget
