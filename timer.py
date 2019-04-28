




import counter

class Timer:
	tac = 0
	tma = 0
	tima = None

	div = counter.Counter(16384)
	
	def __init__(self, interruptManager):
		self.interruptManager = interruptManager
		self.setTima()

	def tick(self):
		self.div.tick()
		if ((self.tac & (1 << 2)) != 0):
			updated = self.tima.tick()
			if (updated and self.tima.getCounter() == 0):
				self.tima.setCounter(self.tma)
				self.interruptManager.requestInterrupt(self.interruptManager.get("Timer"))
	
	def setTima(self):
		value = self.tac & 0b11
		if(value == 0b00):
			self.tima = counter.Counter(4096)
		elif(value == 0b01):
			self.tima = counter.Counter(262144)
		elif(value == 0b10):
			self.tima = counter.Counter(65536)
		elif(value == 0b11):
			self.tima = counter.Counter(16384)




	def setByte(self, address, value):
		if(address == 0xff04):
			self.div.resetCounter()
		elif(address == 0xff05):
			self.tima.resetCounter()
		elif(address == 0xff06):
			self.tma = value
		elif(address == 0xff07):
			self.tac = value
			self.setTima()

	def getByte(self, address):
		if(address == 0xff04):
			return self.div.getCounter()
		elif(address == 0xff05):
			return self.tima.getCounter()
		elif(address == 0xff06):
			return self.tma
		elif(address == 0xff07):
			return self.tac
		raise Exception("Bad code in getbyte timer")









