

class flags():
	def __init__(self):
		self.flags = 0	
		self.Z_POS = 7
		self.N_POS = 6
		self.H_POS = 5
		self.C_POS = 4

	def flagbytes(self):
		return self.flags

	def isZ(self):
		return ((self.flags & (1 << self.Z_POS)) != 0)

	def isN(self):
		return ((self.flags & (1 << self.N_POS)) != 0)

	def isH(self):
		return ((self.flags & (1 << self.H_POS)) != 0)

	def isC(self):
		return ((self.flags & (1 << self.C_POS)) != 0)


	def setZ(self, state):
		if not ((0 <= self.flags <= 0xff)):
			raise Exception("Bad bytes in register")
		if(state):
			self.flags = (self.flags | (1 << self.Z_POS)) & 0xff
		else:
			self.flags = ~(1 << self.Z_POS) & self.flags & 0xff

	def setN(self, state):
		if not ((0 <= self.flags <= 0xff)):
			raise Exception("Bad bytes in register")
		if(state):
			self.flags = (self.flags | (1 << self.N_POS)) & 0xff
		else:
			self.flags = ~(1 << self.N_POS) & self.flags & 0xff

	def setH(self, state):
		if not ((0 <= self.flags <= 0xff)):
			raise Exception("Bad bytes in register")
		if(state):
			self.flags = (self.flags | (1 << self.H_POS)) & 0xff
		else:
			self.flags = ~(1 << self.H_POS) & self.flags & 0xff

	def setC(self, state):
		if not ((0 <= self.flags <= 0xff)):
			raise Exception("Bad bytes in register")
		if(state):
			self.flags = (self.flags | (1 << self.C_POS)) & 0xff
		else:
			self.flags = ~(1 << self.C_POS) & self.flags & 0xff

	def setFlagByte(self, flagsval):
		if not ((0 <= flagsval <= 0xff)):
			raise Exception("Bad bytes in register")
		self.flags = (flagsval & 0xf0)# >> 4) << 4
		#& 0xf0 # BLAGGERS

class register():
	#	For opcodes
	#	http://www.geocities.co.jp/Bookend/5829/soft/emugb/gb_opcode.htm
	def __init__(self):
		#	Internal 8-Bit resigeters
		self.A = 0
		self.B = 0
		self.C = 0
		self.D = 0
		self.E = 0
		self.F = 0
		self.H = 0
		self.L = 0
		#	16 bit rgsters
		self.PC = 0
		self.SP = 0

		self.localflags = flags()		
		self.ime = False

		self.debug = False

		'''
		self.PC = 0#0x01B0
		self.SP = 0xFFFE

		self.setAF(0x1180)
		self.setBC(0x0000)
		self.setDE(0xFF56)
		self.setHL(0x000D)
		'''


		'''
		// Init CPU and its registers to the initial values.
		func (cpu *CPU) Init(cgb bool) {
			cpu.PC = 0x100
			if cgb {
				cpu.AF.Set(0x1180)
			} else {
				cpu.AF.Set(0x01B0)
			}
			cpu.BC.Set(0x0000)
			cpu.DE.Set(0xFF56)
			cpu.HL.Set(0x000D)
			cpu.SP.Set(0xFFFE)

			cpu.AF.Mask = 0xFFF0
		}
		'''



	def setRegister(self, registerName,addressspace,args, value, call=False):
		if not call:
			return lambda : self.setRegister(registerName,addressspace, args, value, call=True)
		
		if(len(registerName) == 1):
			if not ((0 <= value <= 0xff)):
				raise Exception("Bad bytes in register")
		if(len(registerName) == 2):
			if not ((0 <= value <= 0xffff)):
				raise Exception("Bad word in register")

		if(registerName == "A"):
			self.A = value
		elif(registerName == "B"):
			self.B = value
		elif(registerName == "C"):
			self.C = value
		elif(registerName == "D"):
			self.D = value
		elif(registerName == "E"):
			self.E = value
		elif(registerName == "H"):
			self.H = value
		elif(registerName == "L"):
			self.L = value
		elif(registerName == "AF"):
			self.setAF(value)
		elif(registerName == "BC"):
			self.setBC(value)
		elif(registerName == "DE"):
			self.setDE(value)
		elif(registerName == "HL"):
			self.setHL(value)
		elif(registerName == "SP"):
			self.setSP(value)
		elif(registerName == "PC"):
			self.setPC(value)
		elif(registerName == "d8"):
			raise Exception("bad code called in setRegister")
		elif(registerName == "d16"):
			raise Exception("bad code called in setRegister")
		elif(registerName == "r8"):
			raise Exception("bad code called in setRegister")
		elif(registerName == "a16"):
			raise Exception("bad code called in setRegister")
		elif(registerName == "(BC)"):
			addressspace.setByte(self.getBC(), value)
		elif(registerName == "(DE)"):
#			print(self.getDE())
#			print(self.getDE())
#			print(addressspace)
			addressspace.setByte(self.getDE(), value)
		elif(registerName == "(HL)"):
			addressspace.setByte(self.getHL(), value)
		elif(registerName == "(a8)"):
			addressspace.setByte(0xff00 | args[0], value)
		elif(registerName == "(a16)"):
			addressspace.setByte(toword(args), value)
		elif(registerName == "(C)"):
			addressspace.setByte(0xff00 | self.getC(), value)
		
	'''

saveopcode(0, 0xe0, 12, 1, "LDH (n), A", lambda registers, addressspace, funksjonsargumenter : addressspace.setByte(0xff00 | funksjonsargumenter[0], registers.getA() ))						# (r, m, a) -> m.setByte(0xff00 + a[0], r.getA()));
#	"LDH A, (n)",
saveopcode(0, 0xf0, 12, 1, "LDH A, (n)", lambda registers, addressspace, funksjonsargumenter : registers.setA(addressspace.getByte(0xff00 | funksjonsargumenter[0]) ) )						# (r, m, a) -> r.setA(m.getByte(0xff00 + a[0])));


	'''

		
			
	def getRegister(self, registerName,addressspace,args, call=False):
		if not call:
			return lambda : self.getRegister(registerName, call=True)
		if(registerName == "A"):
			return self.A
		elif(registerName == "B"):
			return self.B
		elif(registerName == "C"):
			return self.C 
		elif(registerName == "D"):
			return self.D 
		elif(registerName == "E"):
			return self.E 
		elif(registerName == "H"):
			return self.H 
		elif(registerName == "L"):
			return self.L 
		elif(registerName == "AF"):
			return self.getAF()
		elif(registerName == "BC"):
			return self.getBC()
		elif(registerName == "DE"):
			return self.getDE()
		elif(registerName == "HL"):
			return self.getHL()
		elif(registerName == "SP"):
			return self.getSP()
		elif(registerName == "PC"):
			return self.getPC()
		elif(registerName == "d8"):
			return args[0]
		elif(registerName == "d16"):
			return toword(args)
		elif(registerName == "r8"):
			return args[0]
		elif(registerName == "a16"):
			return toword(args)
		elif(registerName == "(BC)"):
			return addressspace.getByte(self.getBC())
		elif(registerName == "(DE)"):
			return addressspace.getByte(self.getDE())
		elif(registerName == "(HL)"):
			return addressspace.getByte(self.getHL())
		elif(registerName == "(a8)"):
			return addressspace.getByte(0xff00 | args[0])
		elif(registerName == "(a16)"):
			return addressspace.getByte(toword(args))
		elif(registerName == "(C)"):
			return addressspace.getByte(0xff00 | self.getC())
		
	



	#	Writing to registers
	def setA(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad bytes in register")
		self.A = value

	def setB(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad bytes in register")
		self.B = value

	def setC(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad bytes in register")
		self.C = value

	def setD(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad bytes in register")
		self.D = value

	def setE(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad bytes in register")
		self.E = value

	def setH(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad bytes in register")
		self.H = value

	def setL(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad bytes in register")
		self.L = value


	def setAF(self, value):
		if not ((0 <= value <= 0xffff)):
			raise Exception("Bad word in register")
		self.A = (value >> 8)
		
		#self.F = (value & 0xff) & 0xf0
		
		self.localflags.setFlagByte(getLSB(value))

		#getLSB(value & 0xf0) 

#		print( (getLSB(value) & 0xf0) == ((value & 0xf0) & 0xff) )
#		self.localflags.setFlagByte(getLSB(value))

	def setBC(self, value):
		if not ((0 <= value <= 0xffff)):
			raise Exception("Bad word in register")
		self.B = (value >> 8)
		self.C = (value & 0xff)


	def setDE(self, value):
		if not ((0 <= value <= 0xffff)):
			raise Exception("Bad word in register")
		self.D = (value >> 8)
		self.E = (value & 0xff)

	def setHL(self, value):
		if not ((0 <= value <= 0xffff)):
			raise Exception("Bad word in register")
		self.H = (value >> 8)
		self.L = (value & 0xff)

	def setSP(self, value):
		if not ((0 <= value <= 0xffff)):
			raise Exception("Bad word in register")
		self.SP = value

	def setPC(self, value):
		if not ((0 <= value <= 0xffff)):
			raise Exception("Bad word in register")
		self.PC = value

	def setIME(self, value):
		if not type(value) == bool:
			raise Exception("bad arguemtn for setIME")
		self.ime = value


	def decrementHL(self):
		old = self.getHL()
		self.setHL((old - 1)  % 0xffff)
#		print(old)
		return old

	def incrementHL(self):
		old = self.getHL()
		self.setHL((old + 1)  % 0xffff)
		return old
	
	def decrementSP(self):
		self.SP = (self.SP - 1) % 0xffff
	
	def incrementSP(self):
		self.SP = (self.SP + 1) % 0xffff

	def incrementPC(self):	
		self.PC = (self.PC + 1) % 0xffff




	def flagsstatus(self):
		newFlags = ""
		for flagsarr in 	[
								[self.localflags.isZ(), "Z"],
								[self.localflags.isN(), "N"],
								[self.localflags.isH(), "H"],
								[self.localflags.isC(), "C"]
							]:
			if(flagsarr[0]):
				newFlags += flagsarr[1]# + "-"
			else:
				newFlags += "-"
		return newFlags

	def getStatus(self):
		def setZeros(var):
			return (4-len(var)) * "0" + var


		AF = setZeros(hex(self.getAF()).replace("0x", ""))
		BC = setZeros(hex(self.getBC()).replace("0x", ""))
		DE = setZeros(hex(self.getDE()).replace("0x", ""))
		HL = setZeros(hex(self.getHL()).replace("0x", ""))
		SP = setZeros(hex(self.getSP()).replace("0x", ""))
		PC = setZeros(hex(self.getPC()).replace("0x", ""))



		string = ("AF={}, BC={}, DE={}, HL={}, SP={}, PC={}".format(AF, BC, DE, HL, SP, PC))
	#	string = string.replace("0x","")
		newFlags = self.flagsstatus()		
		string += (", {}{}".format(newFlags ,((8-len(newFlags)) * "-")))
		return string

	#	Reading the registers
	def getA(self):
		return self.A	

	def getB(self):
		return self.B

	def getC(self):
		return self.C

	def getD(self):
		return self.D

	def getE(self):
		return self.E

	def getF(self):
		return self.F

	def getH(self):
		return self.H

	def getL(self):
		return self.L

	def getAF(self):
		#return (self.getA() << 8 | self.getF())
		#self.localflags.flagbytes())#self.getF() )
		return (self.getA() << 8 | self.localflags.flagbytes() )# self.localflags.flagbytes())

	def getBC(self):
		return (self.getB() << 8 | self.getC())

	def getDE(self):
		return (self.getD() << 8 | self.getE())
	
	def getHL(self):
		return (self.getH() << 8 | self.getL())

	def getSP(self):
		return (self.SP)

	def getPC(self):
		return (self.PC)

	def getFlags(self):
		return self.localflags.flags

	def isIME(self):
		return self.ime






	'''
		Operations
	'''
	def addbytes(self, byte1, byte2):
		if not ((0 <= byte1 <= 0xff) or (0 <= byte2 <= 0xff)):
			raise Exception("Bad bytes in addbytes")
		self.localflags.setZ(((byte1 + byte2 ) & 0xff == 0))
		self.localflags.setN(False)
		self.localflags.setH(((byte1 & 0x0f) + (byte2 & 0x0f) > 0x0f))
		self.localflags.setC(((byte1 + byte2 > 0xff)))
		return ((byte1 + byte2) & 0xff )

	def addBytesAndCarry(self, byte1, byte2):
		if not ((0 <= byte1 <= 0xff) or (0 <= byte2 <= 0xff)):
			raise Exception("Bad bytes in addbytes")
		cary = 1 if(self.localflags.isC()) else 0
		self.localflags.setZ((byte1 + byte2 + cary ) & 0xff == 0)
		self.localflags.setN(False)
		self.localflags.setH(((byte1 & 0x0f) + (byte2 & 0x0f) + cary > 0x0f))
		self.localflags.setC(((byte1 + byte2 + cary > 0xff)))
		return ((byte1 + byte2 + cary) & 0xff )

	def subytes(self, byte1, byte2):
		if not ((0 <= byte1 <= 0xff) or (0 <= byte2 <= 0xff)):
			raise Exception("Bad bytes in addbytes")
		self.localflags.setZ(((byte1 - byte2 ) & 0xff == 0))
		self.localflags.setN(True)
		self.localflags.setH((0x0f & byte2) > (0x0f & byte1))
		self.localflags.setC(((byte2 > byte1)))
		return ((byte1 - byte2) % 0xff )

	def subBytesWithCarry(self, byte1, byte2):
		if not ((0 <= byte1 <= 0xff) or (0 <= byte2 <= 0xff)):
			raise Exception("Bad bytes in addbytes")

		carry = 1 if(self.localflags.isC()) else 0

		self.localflags.setZ(((byte1 - byte2 - carry) & 0xff) == 0)
		self.localflags.setN(True)
		self.localflags.setH(((0x0f & (byte2 + carry)) > (0x0f & byte1)))
		self.localflags.setC((byte2 + carry > byte1))
		return ((byte1 - byte2 - carry) % 0xff)

	def bitAnd(self, byte1, byte2):
		if not ((0 <= byte1 <= 0xff) or (0 <= byte2 <= 0xff)):
			raise Exception("Bad bytes in addbytes")

		result = byte1 & byte2;
		self.localflags.setZ((result == 0))
		self.localflags.setN((False))
		self.localflags.setH((True))
		self.localflags.setC((False))
		return result


	def bitOr(self, byte1, byte2):
		if not ((0 <= byte1 <= 0xff) or (0 <= byte2 <= 0xff)):
			raise Exception("Bad bytes in addbytes")

		result = byte1 | byte2;
		self.localflags.setZ((result == 0))
		self.localflags.setN((False))
		self.localflags.setH((False))
		self.localflags.setC((False))
		return result

	def bitXor(self, byte1, byte2):
		if not ((0 <= byte1 <= 0xff) or (0 <= byte2 <= 0xff)):
			raise Exception("Bad bytes in addbytes")

		result = byte1 ^ byte2;
		self.localflags.setZ((result == 0))
		self.localflags.setN((False))
		self.localflags.setH((False))
		self.localflags.setC((False))
		return result


	def INC(self,flags, byte):
		if not ((0 <= byte <= 0xff)):
			raise Exception("Bad bytes in addbytes")

		result = (byte + 1) & 0xff;
		self.localflags.setZ((result == 0))
		self.localflags.setN((False))
		self.localflags.setH(((0x0f & result) < (0x0f & byte)))
		return result

	def DEC(self, flags, byte):
		if not ((0 <= byte <= 0xff)):
			raise Exception("Bad bytes in addbytes")

		result = (byte - 1) & 0xff;
		self.localflags.setZ((result == 0))
		self.localflags.setN((True))
		self.localflags.setH((byte & 0x0f ) == 0)
		return result


	def addSignedByteToWord(self, word, signedbyte):
		if not ((0 <= signedbyte <= 0xff)):
			raise Exception("Bad bytes in addSignedByteToWord")
		if not ((0 <= word <= 0xffff)):
			raise Exception("Bad word in addSignedByteToWord")

		self.localflags.setZ(False)
		self.localflags.setN(False)
		def abs(byte):
			if((byte & (1 << 7)) != 0):
				return 0x100 - byte
			else:
				return byte

		b = abs(byte)

		if((signedbyte & (1 << 7)) != 0):
			self.localflags.setH( (word & 0x0f) < (b & 0x0f) )
			self.localflags.setC( (word & 0xff) < (b) )
			return (word-b) % 0xffff
		else:
			self.localflags.setC((word & 0xff) + b > 0xff)
			self.localflags.setH((word & 0x0f) + (b & 0x0f) > 0x0f)
			return (word+b) & 0xffff

	def addWords(self, word1, word2):
		if not ((0 <= word1 <= 0xffff) or (0 <= word2 <= 0xffff)):
			raise Exception("Bad word in addSignedByteToWord")
		self.localflags.setN(False)
		self.localflags.setH((word1 & 0x0fff) + (word2 & 0x0fff) > 0x0fff)
		self.localflags.setC(word1 + word2 > 0xffff)
		return (word1 + word2) & 0xffff;

	def swap(self, flags, byteValue):
		if not ((0 <= byteValue <= 0xff)):
			raise Exception("Bad bytes in swap")
		upper = byteValue & 0xf0;
		lower = byteValue & 0x0f;
		result = (lower << 4) | (upper >> 4)
		self.localflags.setZ(result == 0)
		self.localflags.setN(False)
		self.localflags.setH(False)
		self.localflags.setC(False)
		return result

	def rotateLeft(self, byteValue):
		if not ((0 <= byteValue <= 0xff)):
			raise Exception("Bad bytes in swap")

		result = (byteValue << 1) & 0xff;
		if ((byteValue & (1<<7)) != 0): 
			result |= 1;
			self.localflags.setC(True)
		else: 
			self.localflags.setC(False)   
		self.localflags.setZ(result == 0)
		self.localflags.setN(False)
		self.localflags.setH(False)
		return result

	def rotateRight(self, byteValue):
		if not ((0 <= byteValue <= 0xff)):
			raise Exception("Bad bytes in swap")

		result = (byteValue >> 1);
		if ((byteValue & (1<<7)) != 0):
			result |= 1;
			self.localflags.setC(True)
		else: 
			self.localflags.setC(False)   
		self.localflags.setZ(result == 0)
		self.localflags.setN(False)
		self.localflags.setH(False)
		return result

	def rotateLeftThroughCarry(self, flags, byteValue):
		if not ((0 <= byteValue <= 0xff)):
			raise Exception("Bad bytes in swap")
		
		result = (byteValue << 1) & 0xff
		result |= (1 if(self.localflags.isC()) else 0)
		#print((byteValue & (1<<7)) != 0)
		self.localflags.setC((byteValue & (1<<7)) != 0)
		self.localflags.setZ(result == 0)
		self.localflags.setN(False)
		self.localflags.setH(False)
		return result

#	https://www.reddit.com/r/EmuDev/comments/6mobks/question_gameboy_f_register_bug/
#	^ her er sannheten?


	def rotateRightThroughCarry(self, byteValue):
		if not ((0 <= byteValue <= 0xff)):
			raise Exception("Bad bytes in swap")
		
		result = byteValue >> 1
		result |=  (1 << 7) if(flags.isC()) else 0
		self.localflags.setC((byteValue & 1) != 0)
		self.localflags.setZ(result == 0)
		self.localflags.setN(False)
		self.localflags.setH(False)
		return result

	def shiftLeft(self, byteValue):
		if not ((0 <= byteValue <= 0xff)):
			raise Exception("Bad bytes in swap")
		
		result = (byteValue << 1) & 0xff
		self.localflags.setC((byteValue & (1<<7)) != 0)
		self.localflags.setZ(result == 0)
		self.localflags.setN(False)
		self.localflags.setH(False)
		return result

	def shiftRightArtithmetic(self, byteValue):
		if not ((0 <= byteValue <= 0xff)):
			raise Exception("Bad bytes in swap")
		
		result = (byteValue >> 1) | (byteValue & (1 << 7))
		self.localflags.setC((byteValue & 1) != 0)
		self.localflags.setZ(result == 0)
		self.localflags.setN(False)
		self.localflags.setH(False)
		return result

	def shiftRightLogical(self, byteValue):
		if not ((0 <= byteValue <= 0xff)):
			raise Exception("Bad bytes in swap")
		
		result = (byteValue >> 1)
		self.localflags.setC((byteValue & 1) != 0)
		self.localflags.setZ(result == 0)
		self.localflags.setN(False)
		self.localflags.setH(False)
		return result


	def bit(self,flags, byteValue, bit):
		if not ((0 <= byteValue <= 0xff) or (0 <= bit <= 0xff)):
			raise Exception("Bad bytes in swap")

		if(bit < 8):
			self.localflags.setZ((byteValue & (1 << bit)) != 0)

		self.localflags.setN(False)
		self.localflags.setH(True)


	def setBit(self, byteValue, position):		
		if not ((0 <= byteValue <= 0xff)):
			raise Exception("Bad bytes in swap")
		return (byteValue | (1 << position)) & 0xff

	def clearBit(self, byteValue, position):		
		if not ((0 <= byteValue <= 0xff)):
			raise Exception("Bad bytes in swap")
		return  ~(1 << position) & byteValue & 0xff

	def push(self, registers, addressspace, word):
		if not ((0 <= word <= 0xffff)):
			raise Exception("Bad word in push")

	#	print(word)
		self.decrementSP()
#		addressspace.setByte(self.getSP(), getMSB(word))
		addressspace.setByte(self.getSP(), (word & 0xff00) >> 8)
		self.decrementSP()
#		addressspace.setByte(self.getSP(), getLSB(word))
		addressspace.setByte(self.getSP(), (word & 0x00ff))
		

	def pop(self, addressspace):
#		print(self.getSP())
#		print(addressspace.getByte(self.getSP(), True))
		lsb = addressspace.getByte(self.getSP())
		self.incrementSP()
		msb = addressspace.getByte(self.getSP())
		self.incrementSP()
		#print("ALL ZERO?")
		#print(lsb | (msb << 8))

		

		return lsb | (msb << 8);

	def call(self, registers, addressspace, address):
		if not ((0 <= address <= 0xff)):
			raise Exception("Bad bytes in rest")
		#	def load -> pc


		self.push(registers, addressspace, (registers.getPC()) & 0xffff);
		self.setPC(address);

	def reset(self, registers, addressspace, address):
		if not ((0 <= address <= 0xff)):
			raise Exception("Bad bytes in rest")
		self.push(registers, addressspace, address)
		self.setPC(address)

	def ret(self, registers, addressspace):
		#print(self.pop(addressspace))
		self.setPC(self.pop(addressspace))



def getLSB(word):
	if not ((0 <= word <= 0xffff)):
		raise Exception("Bad word in addSignedByteToWord")
	return (word & 0xff)

def getMSB(word):
	if not ((0 <= word <= 0xffff)):
		raise Exception("Bad word in addSignedByteToWord")
	return (word >> 8)	

def towordint(msb, lsb):
	if not ((0 <= msb <= 0xff) or (0 <= lsb <= 0xff)):
		raise Exception("Bad bytes in toword")
	return (msb << 8) | lsb

def toword(arr):
	return towordint(arr[1], arr[0])

