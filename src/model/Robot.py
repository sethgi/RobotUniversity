import utils
import sympy.geometry as geometry

class Robot:
	"""
	Encodes robots and robot dynamics
	"""
	def __init__(self, robotConfig: dict) -> None:
		position = utils.loadListSafe(robotConfig, "position", 2)
		x,y = position

		self.position = geometry.Point(position)

		self.theta = utils.loadSafe(robotConfig, "theta")

		self.xVelocity, self.yVelocity, self.thetaVelocity = 0,0,0
		

		self.hasLeftTorpedo = utils.loadSafe(robotConfig, "leftTorpedo",\
																			 strict=False, default=False)

		self.hasRightTorpedo = utils.loadSafe(robotConfig, "rightTorpedo",\
																			 strict=False, default=False)

		self.gripperState = utils.loadSafe(robotConfig, "gripperState", \
																		strict=False, default=False)
		self.grippedItem	= None
		
		self.width = utils.loadSafe(robotConfig, "width")
		self.height = utils.loadSafe(robotConfig, "height")

		
		self.boundingBox = utils.makeBoundingBox(x,y,self.width, self.height, self.theta)

	def nonlinearDynamics(self, xForce, yForce, thetaForce):
		"""
		simple dynamics:
			
			x_t = x_{t-1} + v.x_{t-1} * 


		"""

		pass
