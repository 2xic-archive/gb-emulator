import os
import sys
sys.path.append("/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1]) + "/")


class operation:
	def __init__(self, read=False, write=False, length=0, execution=None, prooced=None,datalog=None,switchInterrupts=None):
		#	needed for cycles
		self.readMemory = read
		self.writeMemory = write
		self.argsLength = length

		if(execution == None):
			self.exectuionFunction = lambda r,g,b,d : None
		else:
			self.exectuionFunction = execution


		self.datalog = datalog

		if(switchInterrupts == None):
			self.switchInterrupts = lambda x : True
		else:
			self.switchInterrupts = switchInterrupts


		self.returnvalue = None
		if(prooced == None):
			self.prooced = lambda x : True
		else:
			self.prooced = prooced

	def execute(self, reg, adr,args, context):
		z = self.exectuionFunction(reg, adr, args, context)
		self.returnvalue = z
		if(z == None):
			return context
		return z

	def getReturnValue(self):
		return self.returnvalue

#if __name__ == "__main__":
if(True):
	import cpuhelper
	import arguments
	import opcodeConstruction
	#

	def regLoad(arr, opcode, target, source):
		return regCmd(arr, opcode, "LD {}, {}".format(target, source)).copyByte(target, source)

	def regCmd(arr, opcode, label):
		if(arr[opcode] != None):
			raise execution("Double opcode ...")

		Builder = opcodeConstruction.create(opcode, label)
		#print(Builder)
		arr[opcode] = Builder
		return Builder

	opcodes = [None]  * 0x100
	extOpcodes = [None] * 0x100

	def buildLoop(startindex, delta, arr):
		index = startindex
		for x in arr:
			yield (index, x)
			index += delta

	for x in buildLoop(0x01, 0x10, ["BC", "DE", "HL", "SP"] ):
		regLoad(opcodes, x[0], x[1], "d16")


	for x in buildLoop(0x06, 0x08, ["B", "C", "D", "E", "H", "L", "(HL)", "A"] ):
		regLoad(opcodes, x[0], x[1], "d8")

	for x in buildLoop(0x02, 0x10, ["(BC)", "(DE)"] ):
		regLoad(opcodes, x[0], x[1], "A")

	for x in buildLoop(0x03, 0x10, ["BC", "DE", "HL", "SP"] ):
		regCmd(opcodes, x[0], "INC {}".format(x[1]) ).load(x[1]).alu("INC").store(x[1])


	for x in buildLoop(0x04, 0x08, ["B", "C", "D", "E", "H", "L", "(HL)", "A"]):
		regCmd(opcodes, x[0], "INC {}".format(x[1]) ).load(x[1]).alu("INC").store(x[1]);
	#	print(x[1])
	#	print(x[0])

	for x in buildLoop(0x05, 0x08, ["B", "C", "D", "E", "H", "L", "(HL)", "A"]):
		regCmd(opcodes, x[0],"DEC {}".format(x[1])).load(x[1]).alu("DEC").store(x[1])
	
	for x in buildLoop(0x07, 0x08, ["RLC", "RRC", "RL", "RR"]):
		regCmd(opcodes, x[0], x[1] + "A").load("A").alu(x[1]).store("A")

	regLoad(opcodes, 0x08, "(a16)", "SP");

	for  x in buildLoop(0x09, 0x10, ["BC", "DE", "HL", "SP"]):
		regCmd(opcodes, x[0], "ADD HL,{}".format(x[1])).load("HL").alu("ADD", x[1]).store("HL")

	for  x in buildLoop(0x0a, 0x10, ["(BC)", "(DE)"]):
		regLoad(opcodes, x[0], "A", x[1])

	for  x in buildLoop(0x0b, 0x10, ["BC", "DE", "HL", "SP"]):
		regCmd(opcodes, x[0], "INC {}".format(x[1])).load(x[1]).alu("DEC").store(x[1])

	regCmd(opcodes, 0x10, "STOP");
	regCmd(opcodes, 0x18, "JR r8").load("PC").alu("ADD", "r8").store("PC");


	for  x in buildLoop(0x20, 0x08, ["NZ", "Z", "NC", "C"]):
		regCmd(opcodes, x[0], "JR {},r8".format(x[1])).load("PC").proceedIf(x[1]).alu("ADD", "r8").store("PC");

	regCmd(opcodes, 0x22, "LD (HL+),A").copyByte("(HL)", "A").load("HL").alu("INC").store("HL");
	regCmd(opcodes, 0x2a, "LD A,(HL+)").copyByte("A", "(HL)").load("HL").alu("INC").store("HL");

	regCmd(opcodes, 0x27, "DAA").load("A").alu("DAA").store("A");
	regCmd(opcodes, 0x2f, "CPL").load("A").alu("CPL").store("A");

	#regCmd(opcodes, 0x32, "LD (HL-),A").copyByte("(HL)", "A").load("HL").alu("DEC").store("HL");
	regCmd(opcodes, 0x32, "LD (HL-),A").copyByte("(HL)", "A").load("HL").alu("DEC").store("HL");

	regCmd(opcodes, 0x0, "NOP")

	regCmd(opcodes, 0x3a, "LD A,(HL-)").copyByte("A", "(HL)").load("HL").alu("DEC").store("HL");

	regCmd(opcodes, 0x37, "SCF").load("A").alu("SCF").store("A");
	regCmd(opcodes, 0x3f, "CCF").load("A").alu("CCF").store("A");


	for t in buildLoop(0x40, 0x08, ["B", "C", "D", "E", "H", "L", "(HL)", "A"]):
		for s in buildLoop(t[0], 0x01, ["B", "C", "D", "E", "H", "L", "(HL)", "A"]):
			if (s[0] == 0x76):
				continue
			#print(t[1])
			regLoad(opcodes, s[0], t[1], s[1]);
			#	regLoad(opcodes, x[0], "A", x[1])
	regCmd(opcodes, 0x76, "HALT");

	for o in buildLoop(0x80, 0x08, ["ADD", "ADC", "SUB", "SBC", "AND", "XOR", "OR", "CP"]):
		for t in buildLoop(o[0], 0x01, ["B", "C", "D", "E", "H", "L", "(HL)", "A"]):
			regCmd(opcodes, t[0], o[1] + " " + t[1]).load("A").alu(o[1], t[1]).store("A")

	for  x in buildLoop(0xc0, 0x08, ["NZ", "Z", "NC", "C"]):
		regCmd(opcodes, x[0], "RET {}".format(x[1])).proceedIf(x[1]).pop().store("PC");

	for  x in buildLoop(0xc1, 0x10, ["BC", "DE", "HL", "AF"]):
		regCmd(opcodes, x[0], "POP {}".format(x[1])).pop().store(x[1]);

	for  x in buildLoop(0xc2, 0x08, ["NZ", "Z", "NC", "C"]):
		regCmd(opcodes, x[0], "JP {},a16".format(x[1])).load("a16").proceedIf(x[1]).store("PC");

	regCmd(opcodes, 0xc3, "JP a16").load("a16").store("PC");

	for  x in buildLoop(0xc4, 0x08,["NZ", "Z", "NC", "C"]):
		regCmd(opcodes, x[0], "CALL {},a16".format(x[1])).proceedIf(x[1]).load("PC").push().load("a16").store("PC");

	for  x in buildLoop(0xc5, 0x10, ["BC", "DE", "HL", "AF"]):
		regCmd(opcodes, x[0], "PUSH {}".format(x[1])).load(x[1]).push();

	for  x in buildLoop(0xc6, 0x08, ["ADD", "ADC", "SUB", "SBC", "AND", "XOR", "OR", "CP"]):
		regCmd(opcodes, x[0], x[1] + " d8").load("A").alu(x[1], "d8").store("A");


	#for (int i = 0xc7, j = 0x00; i <= 0xf7; i += 0x10, j += 0x10) {
	i = 0xc7
	j = 0x00
	while True:
		if(i > 0xf7):
			break
		#print( ("RST %02XH" % j))
		regCmd(opcodes, i, ("RST %02XH" % j)).load("PC").push().loadWord(j).store("PC");
		#print( ("RST %02XH" % j))
		i += 0x10
		j += 0x10

	regCmd(opcodes, 0xc9, "RET").pop().store("PC");

	regCmd(opcodes, 0xcd, "CALL a16").load("PC").push().load("a16").store("PC");

	i = 0xcf
	j = 0x08
	
	while True:
		if(i > 0xff):
			break
		regCmd(opcodes, i, ("RST %02XH" % j)).load("PC").push().loadWord(j).store("PC");
		i += 0x10
		j += 0x10

	regCmd(opcodes, 0xd9, "RETI").pop().store("PC").switchInterrupts(True, False)

	regLoad(opcodes, 0xe2, "(C)", "A");
	regLoad(opcodes, 0xf2, "A", "(C)");

	regCmd(opcodes, 0xe9, "JP (HL)").load("HL").store("PC");

	
	regCmd(opcodes, 0xe0, "LDH (a8),A").copyByte("(a8)", "A");


	regCmd(opcodes, 0xf0, "LDH A,(a8)").copyByte("A", "(a8)");

	regCmd(opcodes, 0xe8, "ADD SP,r8").load("SP").alu("ADD", "r8").store("SP");
	regCmd(opcodes, 0xf8, "LD HL,SP+r8").load("SP").alu("ADD", "r8").store("HL");

	regLoad(opcodes, 0xea, "(a16)", "A");
	regLoad(opcodes, 0xfa, "A", "(a16)");

	regCmd(opcodes, 0xf3, "DI").switchInterrupts(False, True);
	regCmd(opcodes, 0xfb, "EI").switchInterrupts(True, True);

	regLoad(opcodes, 0xf9, "SP", "HL");

	for  o in buildLoop(0x00, 0x08, ["RLC", "RRC", "RL", "RR", "SLA", "SRA", "SWAP", "SRL"]):
		for t in buildLoop(o[0], 0x01, ["B", "C", "D", "E", "H", "L", "(HL)", "A"]):
			regCmd(extOpcodes, t[0], o[1] + " " + t[1]).load(t[1]).alu(o[1]).store(t[1]);


	for o in buildLoop(0x40, 0x40, ["BIT", "RES", "SET"]):
		for b in range(0, 0x08):
			for t in buildLoop(o[0] + b * 0x08, 0x01, ["B", "C", "D", "E", "H", "L", "(HL)", "A"]):
				regCmd(extOpcodes, t[0], "{} {},{}".format(o[1], b, t[1])).load(t[1]).alu(o[1], b).store(t[1]);

