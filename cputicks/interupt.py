
class interupttype:
	def __init__(self):
		self.respone = {
					"VBlank":0x0040,
					"LCDC":0x0048,
					"Timer":0x0050,
					"Serial":0x0058,
					"P10_13":0x0060
				}		
		self.handler = self.respone["VBlank"]
		self.ordinal = 0
	
	def get(self, handler):
		self.handler = self.respone[handler]
		self.ordinal = self.respone.keys().index(handler)
		return self.respone[handler]

	def getHandler(self):
		return self.handler

	ime = False
	interruptFlag = 0
	interruptEnabled = 0
	interruptRequested = False
	pendingEnableInterrupts = -1
	pendingDisableInterrupts = -1

	def enableInterrupts(self, withDelay):
		if(withDelay):
			self.pendingEnableInterrupts = 1
			self.pendingDisableInterrupts = -1
		else:
			self.ime = True

	def disableInterrupts(self, withDelay):
		if(withDelay):			
			self.pendingEnableInterrupts = -1
			self.pendingDisableInterrupts = 1
		else:
			self.ime = False

	def requestInterrupt(self, type):
		if self.ime:
			self.interruptRequested = True

		old = self.interruptFlag
		self.interruptFlag = old | (1 << self.ordinal);

	def onInstructionFinished(self):
		if (self.pendingEnableInterrupts != -1) :
			if (self.pendingEnableInterrupts == 0) :
				self.ime = True
			self.pendingEnableInterrupts -= 1
			
		if (self.pendingDisableInterrupts != -1):
			if (self.pendingDisableInterrupts == 0):
				self.ime = False
			self.pendingDisableInterrupts -= 1
			
	def isInterruptRequested(self):
		return self.interruptRequested

	def flush(self):
		self.interruptFlag = 0
		self.interruptRequested = False

	def setByte(self,address, value):
		if(address == 0xff0f):
			if(self.ime):
				self.interruptRequested = True
			self.interruptFlag = value
		elif(address == 0xffff):
			self.interruptEnabled = value

	def isInterruptFlagSet(self):
		return (self.interruptFlag & self.interruptEnabled) != 0

	def getByte(self,address):
		if(address == 0xff0f):
			return self.interruptFlag
		elif(address == 0xffff):
			return self.interruptEnabled 

		return 0xff





