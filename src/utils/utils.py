import sys
from PIL import Image
from pathlib import Path
import os
import sympy.geometry as geometry

# Loads the key from the config dictionary, with better exception handling.
# If strict is set, this throws an exception if the key isn't present. 
# If strict is false, then this returns the default value if the key isn't present
def loadSafe(config, key, strict=True, default=None, warnIfMissing=True):
	try:
		result = config[key]
		return result
	except KeyError:
		message = f"Key {key} is not present in the configuration " \
							"Please make sure the config is valid."
		if strict:
			raise Exception(message)
		else:
			if warnIfMissing:
				GameWarn(message)
			return default


# Like loadSafe, but makes sure the result is a list of the correct length
def loadListSafe(config, key, length=None, strict=True, default=None, warnIfMissing=True):
	result = loadSafe(config, key, strict=strict)
	if result is None:
		return default
	
	try:
		realLength = len(result)

		# If enforcing a length, make sure it's right
		if length is not None:
			assert(length == len(result))
		
		return result
	except (TypeError, AssertionError):
		if type(result) != list or length is None:
			correction = "not a valid list"
		else:
			correction = "of length {}".format(len(result))

		message = "Config at key {} is supposed to be a list of length {}, "\
							"but it's actually {}".format(key, length, correction)

		if strict:
			raise Exception(message)
		else:
			if warnIfMissing:
				warn(message)
			return default

# Like loadSafe, but makes sure that the result is a path to a valid image file
def loadImageSafe(config, key):
	result = loadSafe(config, key)
	
	path = os.path.join(Path(__file__).parent.parent, result)
	try:
		img = Image.open(path)
		img.close()
		return path
	except:
		# TODO: Remove 'return path' once images are in place. Ignoring for testing.
		return path
		raise Exception("Image {} not valid".format(key))

def makeBoundingBox(x,y,width,height, theta=0):
		min_x = x-width/2
		max_x = min_x + width

		min_y = y-height/2
		max_y = min_y + height
			
		points = ((min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y))

		# Sympy requires points as individual arguments. *points does this
		# by unpacking the tuple before it's passed to the constructor
		return geometry.Polygon(*points).rotate(theta)
