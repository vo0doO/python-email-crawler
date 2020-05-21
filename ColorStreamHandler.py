import logging
import curses

class ColorStreamHandler(logging.Handler):

	def __init__(self, use_colors):
		logging.Handler.__init__(self)
		self.use_colors = use_colors

		# Инициализировать среду
		curses.setupterm()

		# Получить атрибут цвета переднего плана для этой среды
		self.fcap = curses.tigetstr('setaf')

		# Получить нормальный атрибут
		self.COLOR_NORMAL = curses.tigetstr('sgr0')

		# Get + Сохранить цветовые последовательности
		self.COLOR_INFO = curses.tparm(self.fcap, curses.COLOR_GREEN)
		self.COLOR_ERROR = curses.tparm(self.fcap, curses.COLOR_RED)
		self.COLOR_WARNING = curses.tparm(self.fcap, curses.COLOR_YELLOW)
		self.COLOR_DEBUG = curses.tparm(self.fcap, curses.COLOR_BLUE)

	def color(self, msg, level):
		if level == "INFO":
			return "%s%s%s" % (self.COLOR_INFO, msg, self.COLOR_NORMAL)
		elif level == "WARNING":
			return "%s%s%s" % (self.COLOR_WARNING, msg, self.COLOR_NORMAL)
		elif level == "ERROR":
			return "%s%s%s" % (self.COLOR_ERROR, msg, self.COLOR_NORMAL)
		elif level == "DEBUG":
			return "%s%s%s" % (self.COLOR_DEBUG, msg, self.COLOR_NORMAL)
		else:
			return msg
	
	def emit(self, record):
		record.msg = record.msg.encode('utf-8', 'ignore')
		msg = self.format(record)

		# Это просто удаляет дату и миллисекунды из asctime
		temp = msg.split(']')
		msg = '[' + temp[0].split(' ')[1].split(',')[0] + ']' + temp[1]

		if self.use_colors:
			msg = self.color(msg, record.levelname)
		print msg

# 'record' имеет следующие атрибуты:
# threadName
# name
# thread
# created
# process
# processName
# args
# module
# filename
# levelno
# exc_text
# pathname
# lineno
# msg
# exc_info
# funcName
# relativeCreated
# levelname
# msecs
