import logging

formatter = logging.Formatter("[%(asctime)s] [%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s")

class LevelFilter(logging.Filter):
	def __init__(self, low, high):
		self._low = low
		self._high = high
		logging.Filter.__init__(self)

	def filter(self, record):
		if self._low <= record.levelno <= self._high:
			return True
		return False
