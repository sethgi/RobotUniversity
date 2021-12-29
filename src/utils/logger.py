import logging
import sys
import traceback

def HandleException(*args):
	logging.getLogger().error("Uncaught exception: ", exc_info=args)

sys.excepthook = HandleException

def Info(message):
	logging.getLogger().info(message)

def Warn(message):
	logging.getLogger().warning(message)

def Error(message):
	logging.getLogger().error(message)
