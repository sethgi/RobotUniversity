import sympy.geometry as geometry

from utils import utils

class Robot:
	"""
	Encodes robots and robot dynamics
	"""
	def __init__(self, robotConfig: dict) -> None:
		position = utils.loadListSafe(robotConfig, "position", 2)
		x,y = position

		self._position = geometry.Point(position)

		self._theta = utils.loadSafe(robotConfig, "theta")

		self._x_velocity, self._y_velocity, self._theta_velocity = 0,0,0
		

		self._has_left_torpedo = utils.loadSafe(robotConfig, "leftTorpedo",\
																			 strict=False, default=False)

		self._has_right_torpedo = utils.loadSafe(robotConfig, "rightTorpedo",\
																			 strict=False, default=False)

		self._gripper_state = utils.loadSafe(robotConfig, "gripperState", \
																		strict=False, default=False)
		self._gripped_item	= None
		
		self._width = utils.loadSafe(robotConfig, "width")
		self._height = utils.loadSafe(robotConfig, "height")

		
		self._boundingBox = utils.makeBoundingBox(x,y,self._width, self._height, self._theta)

	def nonlinearDynamics(self, x_force, y_force, theta_torque):
		"""
		simple dynamics:
			
			x_t = x_{t-1} + v.x_{t-1} * 


		"""

		pass
