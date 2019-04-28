


class dma:

	transferInProgress = False
	fromval = 0
	ticks = 0

	def __init__(self, addressSpace):
		self.addressSpace = addressSpace

	def tick(self):
		if(self.transferInProgress):
			self.ticks += 1
			if(self.ticks == 671):
				self.transferInProgress = False
				for i in range(0, 0xa0):
					self.addressSpace.setByte(0xfe00 + i, self.addressSpace.getByte(self.fromval + i))

	def setByte(self, address, value):
		self.fromval = value * 0x100
		self.ticks = 0
		self.transferInProgress = True

	def getByte(self, address):
		return 0