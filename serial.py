



def bitishigh(num, bit):
	return (0 != ((num) & (1 << (bit))))


def getValueOfBits(num, listd):
	minindex = min(listd)#-1
	results = 0
	listd[1] = listd[1] + 1
	for bitposion in range(listd[0], listd[1]):
		realtiveindex = ((bitposion)-minindex)
		if(bitishigh(num, bitposion)):
			results += (0x01 << realtiveindex)
	return results


class serial:
	Debug = False

	transfer = False
	clock = 0

	SB = 0
	SC = 0
	log = ""
	EnableBlattsDebug =False

	def __init__(self):
		pass
#		self.DebuglinkFile.write(3 * "\n")


	def setByte(self, address, value):
		if(self.Debug):
	#		print("Serial access ....	{}		{}	{}".format(hex(address), value, chr(value)))
			if(address == 0xff02):
				self.transfer = bool(getValueOfBits(value, [7,7]) == 1)
				self.SB = value
				self.SC = 0x81
			elif(address == 0xff01):
				self.SB = value
				self.log += chr(value)
			self.SB = self.SB << 1
		pass

	def getByte(self, address):
		if(self.Debug):
			print("huh read?")
		pass






	