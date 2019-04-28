import os
import sys
sys.path.append("/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1]) + "/")

datatypes = {
	
}


class args :
	def __init__(self, label, argslen, memory, datatype):
		self.label = label
		self.argslen = argslen
		self.memory = memory
		self.datatype = datatype

	def read(self, registers, addressSpace, argsument):
		if(self.label == "d8"):
			return argsument[0]
		else:
			return registers.getRegister(self.label,addressSpace, argsument, True)

	def write2(self, registers, addressSpace, argsument, value, roundOne):
		def towordint(msb, lsb):
			if not ((0 <= msb <= 0xff) or (0 <= lsb <= 0xff)):
				raise Exception("Bad bytes in toword")
			return (msb << 8) | lsb

		def toword(arr):
			return towordint(arr[1], arr[0])
		
		if(roundOne == 0):
			addressSpace.setByte(toword(argsument), value & 0x00ff);
		else:
			addressSpace.setByte((toword(argsument) + 1) & 0xffff, (value & 0xff00) >> 8);
		return value

	def write(self, registers, addressSpace, argsument, value):
		if(self.label == "d8"):
			raise Exception("Bad to write to argsument")
		else:
			return registers.setRegister(self.label,addressSpace,argsument, value, True)

'''
	8	Bit registers
'''
datatypes["A"] = args("A", 0, False, "8bit")
datatypes["B"] = args("B", 0, False, "8bit")
datatypes["C"] = args("C", 0, False, "8bit")
datatypes["D"] = args("D", 0, False, "8bit")
datatypes["E"] = args("E", 0, False, "8bit")
datatypes["H"] = args("H", 0, False, "8bit")
datatypes["L"] = args("L", 0, False, "8bit")

'''
	16 Bit	registesr
'''
datatypes["AF"] = args("AF", 0, False, "16bit")
datatypes["BC"] = args("BC", 0, False, "16bit")
datatypes["DE"] = args("DE", 0, False, "16bit")
datatypes["HL"] = args("HL", 0, False, "16bit")
datatypes["SP"] = args("SP", 0, False, "16bit")
datatypes["PC"] = args("PC", 0, False, "16bit")

'''
	
'''
datatypes["d8"] = args("d8", 1, False, "8bit")
datatypes["d16"] = args("d16", 2, False, "16bit")
datatypes["r8"] = args("r8", 1, False, "r8")
datatypes["a16"] = args("a16", 2, False, "16bit")

'''
	memory managment
'''


datatypes["(BC)"] = args("(BC)", 0, True, "8bit")
datatypes["(DE)"] = args("(DE)", 0, True, "8bit")
datatypes["(HL)"] = args("(HL)", 0, True, "8bit")

datatypes["(a8)"] = args("(a8)", 1, True, "8bit")
datatypes["(a16)"] = args("(a16)", 2, True, "8bit")
datatypes["(C)"] = args("(C)", 0, True, "8bit")


def parse(inputid):
	return datatypes[inputid]