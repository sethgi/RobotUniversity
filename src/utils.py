import sys
from PIL import Image
from pathlib import Path
import os

def warn(message):
	print("WARNING: " + message, file=sys.stderr)

def loadSafe(config, key, strict=True, default=None):
	try:
		result = config[key]
		return result
	except KeyError:
		message = "Key {} is not present in the configuration. " \
							"Please make sure the config is valid.".format(key)
		if strict:
			raise Exception(message)
		else:
			warn(message)
			return default


def loadListSafe(config, key, length, strict=True, default=None):
	result = loadSafe(config, key, strict=strict)
	if result is None:
		return default
	
	try:
		assert(length == len(result))
		return result
	except (TypeError, AssertionError):
		if type(result) != list:
			correction = "not a list"
		else:
			correction = "of length {}".format(len(result))

		message = "Config at key {} is supposed to be a list of length {}, "\
							"but it's actually {}".format(key, length, correction)

		if strict:
			raise Exception(message)
		else:
			warn(message)
			return default

def loadImageSafe(config, key):
	result = loadSafe(config, key)
	
	path = os.path.join(Path(__file__).parent.parent, result)
	try:
		img = Image.open(path)
		img.close()
		return path
	except:
		# TODO: Remove 'return path' once images are in place
		return path
		raise Exception("Image {} not valid".format(key))


