

class Counter:
	frequency = 0
	counter = 0
	clocks = 0

	def __init__(self, frequency):
		self.frequency = frequency

	def tick(self):
		self.clocks += 1
		if (self.clocks == 4194304 / self.frequency):
			self.clocks = 0
			self.counter = (self.counter + 1) & 0xff
			return True
		else:
			return False

	def getCounter(self):
		return self.counter

	def resetCounter(self):
		self.counter = 0

	def setCounter(self, counter):
		self.counter = counter


