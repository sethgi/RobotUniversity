from Force import Force, ForceType
import numpy as np

class HydrodynamicForces(Force):
	def __init__(self, robot: "Robot"):
		super().__init__()
		self.setRobot(robot)

	def _computeForce(self) -> ForceType:
		
		# Added mass due to acceleration, using approximation that
		# the robot is a square
		transCoeff = 1.51 * np.pi * self.robot.rho * (self.robot.physics.width)**2
		rotCoeff = 0.234 * np.pi * self.robot.rho * (self.robot.physics.width)**2
		Ma = np.diag([transCoeff, transCoeff, rotCoeff])
		
		Fma = Ma @ self.robot.acceleration 
