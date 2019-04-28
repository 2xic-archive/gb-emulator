
functionlist = {
	
}

def registerfunction(name, dataType1, function, dataType2=None):
	if not type(dataType2).__name__ == 'function':
		functionlist[name + dataType1] = function
	else:
		functionlist[name + dataType1 + function] = dataType2

def find(name, arg1, arg2=None):
	if(arg2 == None):
		return functionlist[name + arg1]
	else:
		return functionlist[name + arg1 + arg2]

def INC(flags, arg):
	result = (arg + 1) & 0xff
	flags.setZ((result == 0))
	flags.setN((False))
	flags.setH((arg & 0x0f) == 0x0f)
	return result

def DEC(flags, arg):
	result = (arg - 1) & 0xff
	flags.setZ((result == 0))
	flags.setN((True))
	flags.setH((arg & 0x0f ) == 0)
	return result

def ADD(flags, arg1, arg2):
	flags.setN(False)
	flags.setH((arg1 & 0x0fff) + (arg2 & 0x0fff) > 0x0fff)
	flags.setC(arg1 + arg2 > 0xffff)
	return (arg1 + arg2) & 0xffff


def isNegative(signedByteValue):
	return (signedByteValue & (1 << 7)) != 0;

def abs(signedByteValue):
	if (isNegative(signedByteValue)):
		return 0x100 - signedByteValue;
	else:
		return signedByteValue;

def ADD2(flags, arg1, arg2):
	flags.setZ(False);
	flags.setN(False);

	b = abs(arg2);
	word = arg1;

	if (isNegative(arg2)):
		flags.setH((word & 0x0f) < (b & 0x0f));
		flags.setC((word & 0xff) < b);
		return (word - b) & 0xffff;
	else:
		flags.setC((word & 0xff) + b > 0xff);
		flags.setH((word & 0x0f) + (b & 0x0f) > 0x0f);
		return (word + b) & 0xffff;


def DAA(flags, arg):
	result = arg
	if (flags.isN()):
		if (flags.isH()):
			result = (result - 6) & 0xff
		if (flags.isC()) :
			result = (result - 0x60) & 0xff
		
	else: 
		if (flags.isH() or (result & 0xf) > 9) :
			result += 0x06
		if (flags.isC() or result > 0x9f) :
			result += 0x60
		
	flags.setH(False)
	if (result > 0xff):
		flags.setC(True)
	result &= 0xff
	flags.setZ(result == 0)
	return result

def CPL(flags, arg):
	flags.setN(False)
	flags.setH(False)
	return (~arg) & 0xff


def SCF(flags, arg):
	flags.setN(False)
	flags.setH(False)
	flags.setC(True)
	return arg

def CCF(flags, arg):
	flags.setN(False)
	flags.setH(False)
	flags.setC(not flags.isC())
	return arg


def ADD3(flags, byte1, byte2):
	flags.setZ(((byte1 + byte2) & 0xff) == 0)
	flags.setN(False)
	flags.setH((byte1 & 0x0f) + (byte2 & 0x0f) > 0x0f)
	flags.setC(byte1 + byte2 > 0xff)
	return (byte1 + byte2) & 0xff

def ADC(flags, byte1, byte2):
	carry = 1 if(flags.isC()) else 0
	flags.setZ(((byte1 + byte2 + carry) & 0xff) == 0)
	flags.setN(False)
	flags.setH((byte1 & 0x0f) + (byte2 & 0x0f) + carry > 0x0f)
	flags.setC(byte1 + byte2 + carry > 0xff)
	return (byte1 + byte2 + carry) & 0xff


def SUB(flags, byte1, byte2):
	flags.setZ(((byte1 - byte2) & 0xff) == 0)
	flags.setN(True)
	flags.setH((0x0f & byte2) > (0x0f & byte1))
	flags.setC(byte2 > byte1)
	return (byte1 - byte2) & 0xff

def SUBC(flags, byte1, byte2):
	carry = 1 if(flags.isC()) else 0
	flags.setZ(((byte1 - byte2 - carry) & 0xff) == 0)
	flags.setN(True)
	flags.setH((0x0f & (byte2 + carry)) > (0x0f & byte1))
	flags.setC(byte2 + carry > byte1)
	return (byte1 - byte2 - carry) & 0xff




'''
HERE
'''

def AND(flags, byte1, byte2):
	result = byte1 & byte2
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(True)
	flags.setC(False)
	return result
def OR(flags, byte1, byte2):
	result = byte1 | byte2
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(False)
	flags.setC(False)
	return result
def XOR(flags, byte1, byte2):
	result = (byte1 ^ byte2) & 0xff
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(False)
	flags.setC(False)
	return result

def CP(flags, byte1, byte2):
	flags.setZ(((byte1 - byte2) & 0xff) == 0)
	flags.setN(True)
	flags.setH((0x0f & byte2) > (0x0f & byte1))
	flags.setC(byte2 > byte1)
	return byte1


def RLC(flags, arg):
	result = (arg << 1) & 0xff
	if ((arg & (1<<7)) != 0):
		result |= 1
		flags.setC(True)
	else:
		flags.setC(False)
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(False)
	return result	

def RRC(flags, arg):
	result = arg >> 1
	if ((arg & 1) == 1):
		result |= (1 << 7)
		flags.setC(True)
	else :
		flags.setC(False)
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(False)
	return result

def RL(flags, arg):
	result = (arg << 1) & 0xff
	result |= 1 if(flags.isC() ) else 0
	flags.setC((arg & (1<<7)) != 0)
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(False)
	return result

def RR(flags, arg):
	result = arg >> 1
	result |=  (1 << 7) if(flags.isC()) else 0
	flags.setC((arg & 1) != 0)
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(False)
	return result

def SLA(flags, arg):
	result = (arg << 1) & 0xff
	flags.setC((arg & (1<<7)) != 0)
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(False)
	return result

def SRA(flags, arg):
	result = (arg >> 1) | (arg & (1 << 7))
	flags.setC((arg & 1) != 0)
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(False)
	return result


def SWAP(flags, arg):
	upper = arg & 0xf0
	lower = arg & 0x0f
	result = (lower << 4) | (upper >> 4)
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(False)
	flags.setC(False)
	return result

def SRL(flags, arg):
	result = (arg >> 1)
	flags.setC((arg & 1) != 0)
	flags.setZ(result == 0)
	flags.setN(False)
	flags.setH(False)
	return result

def BIT(flags, arg1, arg2):
	bit = arg2
	flags.setN(False)
	flags.setH(True)
	if (bit < 8):
		flags.setZ(not getBit(arg1, arg2))
	return arg1


registerfunction("INC", "8bit", lambda flags, arg: INC(flags, arg))
registerfunction("INC", "16bit", lambda flags, arg: (arg + 1) & 0xffff)

registerfunction("DEC", "8bit", lambda flags, arg: DEC(flags, arg))
registerfunction("DEC", "16bit", lambda flags, arg: (arg - 1) & 0xffff)

registerfunction("ADD", "16bit", "16bit", lambda flags, arg1, arg2: ADD(flags, arg1, arg2))
registerfunction("ADD", "16bit", "r8", lambda flags, arg1, arg2: ADD2(flags, arg1, arg2))


registerfunction("DAA", "8bit", lambda flags, arg: DAA(flags, arg))

registerfunction("CPL", "8bit", lambda flags, arg: CPL(flags, arg))
registerfunction("SCF", "8bit", lambda flags, arg: SCF(flags, arg))
registerfunction("CCF", "8bit", lambda flags, arg: CCF(flags, arg))

registerfunction("ADD", "8bit", "8bit", lambda flags, byte1, byte2: ADD3(flags, byte1, byte2))
registerfunction("ADC", "8bit", "8bit", lambda flags, byte1, byte2: ADC(flags, byte1, byte2))

registerfunction("SUB", "8bit", "8bit", lambda flags, byte1, byte2: SUB(flags, byte1, byte2))
registerfunction("SBC", "8bit", "8bit", lambda flags, byte1, byte2: SUBC(flags, byte1, byte2))

registerfunction("AND", "8bit", "8bit", lambda flags, byte1, byte2: AND(flags, byte1, byte2))
registerfunction("OR", "8bit", "8bit", lambda flags, byte1, byte2: OR(flags, byte1, byte2))


registerfunction("XOR", "8bit", "8bit", lambda flags, byte1, byte2: XOR(flags, byte1, byte2))


registerfunction("CP", "8bit", "8bit", lambda flags, byte1, byte2: CP(flags, byte1, byte2))

registerfunction("RLC", "8bit", lambda flags, byte1: RLC(flags, byte1))
registerfunction("RRC", "8bit", lambda flags, byte1: RRC(flags, byte1))
registerfunction("RL", "8bit", lambda flags, byte1: RL(flags, byte1))
registerfunction("RR", "8bit", lambda flags, byte1: RR(flags, byte1))
registerfunction("SLA", "8bit", lambda flags, byte1: SLA(flags, byte1))

registerfunction("SRA", "8bit", lambda flags, byte1: SRA(flags, byte1))
registerfunction("SWAP", "8bit", lambda flags, byte1: SWAP(flags, byte1))
registerfunction("SRL", "8bit", lambda flags, byte1: SRL(flags, byte1))

registerfunction("BIT", "8bit", "8bit", lambda flags, byte1, byte2: BIT(flags, byte1, byte2))


def getBit(byteValue, position):
	return (byteValue & (1 << position)) != 0;

def setBit( byteValue,  position):
	#checkByteArgument("byteValue", byteValue)
	return (byteValue | (1 << position)) & 0xff
	
def clearBit( byteValue,  position):
	#checkByteArgument("byteValue", byteValue)
	return ~(1 << position) & byteValue & 0xff

registerfunction("RES", "8bit", "8bit", lambda flags, byte1, byte2: clearBit(byte1, byte2))
registerfunction("SET", "8bit", "8bit", lambda flags, byte1, byte2: setBit(byte1, byte2))









