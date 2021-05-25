import utils

class Robot:
	def __init__(self, robotConfig: dict) -> None:
		position = utils.loadListSafe(robotConfig, "position", 2)
		self.xPosition, self.yPosition = position

		self.theta = utils.loadSafe(robotConfig, "theta")

		self.xVelocity, self.yVelocity, self.thetaVelocity = 0,0,0

		self.hasLeftTorpedo = utils.loadSafe(robotConfig, "leftTorpedo",\
																			 strict=False, default=False)

		self.hasRightTorpedo = utils.loadSafe(robotConfig, "rightTorpedo",\
																			 strict=False, default=False)

		self.gripperState = utils.loadSafe(robotConfig, "gripperState", \
																		strict=False, default=False)
		self.grippedItem	= None

	
	def nonlinearDynamics(self, xForce, yForce, thetaForce):
		"""
		simple dynamics:
			
			x_t = x_{t-1} + v.x_{t-1} * 


		"""
