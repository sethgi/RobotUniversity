from typing import Union, Tuple
import numpy as np

ForceType = Union[np.array, float]

class Force:
	
	"""
	If axis is None, then this is a 3D wrench and returns a tuple
	(x,y,theta) for the forces in x,y and torque in z (theta).
	"""
	def __init__(self, name: str = None, axis: int=None) -> None:
		if axis is not None:
			if axis < 0 or axis > 2:
				raise Exception("Axis for Force must be None (indicating it's a 3D wrench)"\
										     " or an integer between 0 and 2")
			self.forceType = Tuple[float, float, float]
		else:
			self.forceType = float

		self.axis = axis
		self.id = None
		self.name = name

		self.robot = None

	def setRobot(self, robot: "Robot") -> None:
		self.robot = robot

	def _computeForce(self) -> ForceType:
		raise Exception("Not Implemented: Forces must implement the _computeForce function")

	def getForce(self) -> ForceType:
		if self.robot is None:
			raise Exception("Robot mustbe set with setRobot before calling getForce")

		force = self._computeForce()
		assert isinstance(force, self.forceType), "_computeForce returned the incorrect type"

class TimedForce(Force):
	def __init__(self, name: str = None, axis: int = None, \
							numSteps: int = None, duration: float = None) -> None:
		super().__init__(name, axis)

		self.numSteps = numSteps
		self.duration = duration

		if self.numSteps is not None and self.duration is not None:
			raise Exception("You can't pass both numSteps and duration to TimedForce")
		
		elif self.numSteps is None and self.duration is None:
			self.numSteps = 1
	
		self.stepCounter = 0

	def setRobot(self, robot: "Robot") -> None:
		super().setRobot(robot)

		if self.numSteps is None:
			self.numSteps = np.ceil(self.duration / )
			
	def getForce(self) -> ForceType:
		force = super().getForce()
		self.stepCounter += 1

		if self.stepCounter == self.numSteps:
			self.robot.removeForce(self.id)
	

