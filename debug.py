
import time

class debug:
	validopcodes = []


	breakpoints = []

	def __init__(self, reg, addr):
		self.instructionCount = 0
		self.logevry = 100000


		self.currentTime = time.time()

		self.register = reg
		self.addressapce = addr

		self.oldreg = None


	def tick(self, opcode):
		self.instructionCount += 1
		self.checkBreakpoint(self.instructionCount, opcode)

		if(self.logevry > 0 and self.instructionCount % self.logevry == 0):
			print("{}	{}	{}".format(self.instructionCount, opcode, time.time()-self.currentTime))
			self.currentTime = time.time()
			return True

	def trace(self, opcode):
		registerStatus = self.register.getStatus().split("PC")[0]
		if(registerStatus != self.oldreg):
			print("Opcode : {}".format(opcode.label))
			print(registerStatus)
			self.oldreg = registerStatus


	def addBreakpoint(self, instruction, log=True):
		if(instruction not in self.breakpoints):
			if(type(instruction) == int):
				if(log):
					print("Added breakpoint when instructionCount == {}".format(instruction))
			else:
				opcodeLabel = self.validopcodes[int(instruction, 16)].label
				if(log):
					print("Added breakpoint on instruction '{}'".format(opcodeLabel))
			self.breakpoints.append(instruction)

	def giveOpcodes(self, opcodeList):
		self.validopcodes = opcodeList

	def checkBreakpoint(self, value, currentopcode=None):
		if(value in self.breakpoints):
			def commands():
				print("press [c] to continue, [cc] to continue one instruction, [r] to get register and [q] to exit")
				command = input()
				if(command == "c"):
					pass
				elif(command == "r"):
					print(self.register.getStatus())
				elif(command == "cc"):
					self.addBreakpoint(self.instructionCount + 1, log=False)
				elif(command == "q"):
					print("bye")
					exit(0)
				else:
					return commands()

			print("*breakpoint at {}[{}]*".format(value, currentopcode))
			commands()
