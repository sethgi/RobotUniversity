import logging
import sys
import traceback

# https://docs.python.org/3/library/logging.handlers.html
# Note that as long as I support write() and flush(), anything can be written to 

class Logger:
	def __init__(self, name: str = "RobotUniversity") -> None:
		self._name = name

		self._logger = logging.getLogger(name)
		self._logger.setLevel(logging.INFO)
		self._format = logging.Formatter(fmt=' %(name)s :: %(levelname)-8s :: %(message)s')

		self._console_handler = logging.StreamHandler()
		self._console_handler.setLevel(logging.INFO)
		self._console_handler.setFormatter(self._format)

		self._logger.addHandler(self._console_handler)

	def doLog(self, level, message):
		self._logger.log(level, message)

	def Debug(self, message):
		self.doLog(logging.DEBUG, message)

	def Info(self, message):
		self.doLog(logging.INFO, message)

	def Warn(self, message):
		self.doLog(logging.WARNING, message)

	def Error(self, message):
		self.doLog(logging.ERROR, message)

	def Critical(self, message):
		self.doLog(logging.CRITICAL, message)
