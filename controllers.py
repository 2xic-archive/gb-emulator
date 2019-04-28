



class buttons:
		avaible = {
			"RIGHT":(0x01, 0x10), 
			"LEFT" : (0x02, 0x10), 
			"UP" : (0x04, 0x10), 
			"DOWN" : (0x08, 0x10),
			"A" : (0x01, 0x20), 
			"B" : (0x02, 0x20), 
			"SELECT" : (0x04, 0x20), 
			"START" : (0x08, 0x20)
		}


		line = 0
		mask = 0


		def __init__(self):
			pass

		def getMask(self):
			return self.mask

		def getLine(self):
			return self.line

class joycontrollers:
	def __init__(self, interruptManager):
		self.interruptManager = interruptManager
		self.activeButtons = {}
		self.p1 = 0

		self.buttonids = buttons()

	def buttonPress(self, buttonID):
		self.interruptManager.requestInterrupt(self.interruptManager.get("P10_13"))
		self.activeButtons[buttonID] = self.buttonids.avaible[buttonID]

	def buttonUnPress(self, buttonID):
		self.activeButtons.pop(buttonID, None)

	

	def setByte(self, address, value):
		self.p1 = value & 0b00110000;

	def getByte(self, address):
		result = self.p1 | 0b00001111;
		for buttonid, buttonvalue  in self.activeButtons.items():
			if ((buttonvalue[1] & self.p1) == 0):
				result &=  0xff & ~buttonvalue[0]
		#print(result)
		#print("happy")
		return result







