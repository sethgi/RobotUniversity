# https://docs.python.org/3/library/logging.handlers.html
# Note that as long as I support write() and flush(), anything can be written to 

import logging
import time

ALL_LOGS = {}

LOG_ID = 0
def generateID() -> int:
	global LOG_ID
	LOG_ID += 1
	return LOG_ID - 1

class LogEntry:
	def __init__(self, level: int, message: str, msg_time: float):
		self.level = level
		self.message = message
		self.time = msg_time

class Logger:
	def __init__(self, name: str = "RobotUniversity", log_in_game: bool = False,
							 queue_size: int = 50, queue_level=logging.INFO) -> None:
		self._name = name
		self._id = generateID()

		global ALL_LOGS
		ALL_LOGS[self._id] = self

		self._log = [] # Stores the most recent queue_size messages
		self._queue = [] # Stores the most recent queue_size messages that haven't been consumed
		self._queue_size = queue_size
		self._queue_level = queue_level

	def __del__(self):
		global ALL_LOGS
		ALL_LOGS.pop(self._id)

	def Log(self, level, message):
		log_time = time.time()
		new_entry = LogEntry(level, message, log_time)
		self._log.append(new_entry)
		
		if level >= self._queue_level:
			self._queue.append(new_entry)
			
			while len(self._queue) > self._queue_size:
				self._queue.pop(0)
			
			self.doLog(level, message, log_time)
	
	def doLog(self, level, message, log_time):
		# Intentionally left empty in base class.
		# Override in others. 
		pass

	def Debug(self, message):
		self.Log(logging.DEBUG, message)

	def Info(self, message):
		self.Log(logging.INFO, message)

	def Warn(self, message):
		self.Log(logging.WARNING, message)

	def Error(self, message):
		self.Log(logging.ERROR, message)

	def Critical(self, message):
		self.Log(logging.CRITICAL, message)
