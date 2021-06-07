import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import utils
import sympy.geometry as geometry
from operator import add
from typing import Tuple
import numpy as np
from typing import Type

from Force import Force
from Hydrodynamics import HydrodynamicForces

class Robot:
	"""
	Encodes robots and robot dynamics
	"""
	
	def __init__(self, robotConfig: dict, dt: float = 0.1) -> None:
		position = utils.loadListSafe(robotConfig, "position", 2)
		x,y = position
		
		self.position = geometry.Point(position)
		self.velocity = np.array([0,0,0])
		self.acceleration = np.array([0,0,0])

		self.theta = utils.loadSafe(robotConfig, "theta")

		self.hasLeftTorpedo = utils.loadSafe(robotConfig, "leftTorpedo",\
																			 strict=False, default=False)

		self.hasRightTorpedo = utils.loadSafe(robotConfig, "rightTorpedo",\
																			 strict=False, default=False)

		self.gripperState = utils.loadSafe(robotConfig, "gripperState", \
																		strict=False, default=False)
		self.grippedItem	= None
		
		self.length = utils.loadSafe(robotConfig, "length")
		self.wiself.dth = utils.loadSafe(robotConfig, "wiself.dth")
		self.height = utils.loadSafe(robotConfig, "height")
		
		self.mass = utils.loadSafe(robotConfig, "mass")
		
		self.boundingBox = utils.makeBoundingBox(x,y,self.width, self.height, self.theta)
		
		self.forces = {}
		self.nextForceId = 0

		self.forcesByName = {}
		self.dt = dt

	"""
	force -> a force object

	returns an ID unique in the scope of the robot
	"""
	def registerForce(self, force: Type[Force]) -> int:
		self.forces[self.nextForceId] = force
		
		if force.name is not None:
			self.forcesByName[force.name] = force
		
		force.id = self.nextForceId

		self.nextForceId += 1
		
		return force.id

	def removeForce(self, id: int = None, name: str = None) -> bool:
		if id is None and name is None:
			return False

		if id is not None:
			force = self.forces[id]

			if force is None:
				return False

			del self.forces[id]
			
			name = force.name
			
			if name is not None and name in self.forcesByName:
				del self.forcesByName[name]
			
			return True
		
		if name in self.forcesByName:
			force = self.forcesByName[name]
			id = force.id

			del self.forces[id]
			del self.forcesByName[name]

			return True

		return False

	def _getWrenchVector(self) -> np.array:

		wrench = np.array([0,0,0])

		for force in self.forces.values():
			axis = force.axis
			
			if axis is None:
				wrench += force._computeForce()
			
			else:
				wrench[axis] += force._computeForce()
		
		return wrench


	def _getAcceleration(self) -> np.array:
		"""
		f = ma
		"""

		wrench = self._getWrenchVector()
		return wrench/self.mass

	def _addHydrodynamicForces(self) -> None:
		hydrodynamics = HydrodynamicForces(self)	
		self.registerForce(hydrodynamics)

	def updateState(self) -> None:
		
		self.acceleration = self._getAcceleration()
		
		xA, yA, thA = self.acceleration
		xV, yV, thV = self.velocity

		dX = xV*self.dt + 0.5*xA*self.dt**2
		dY = yV*self.dt + 0.5*yA*self.dt**2
		dTh = thV*self.dt + 0.5*thA*self.dt**2

		distance = geometry.Point([dX, dY, dTh])

		# TODO: angle wrap this
		self.position += distance
	
		self.velocity += self.acceleration*self.dt

		self.velocity = np.array([xV, yV, thV])
