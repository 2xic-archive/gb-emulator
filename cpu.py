
import cpuhelper
import os
import sys
sys.path.append("/".join(os.path.dirname(os.path.realpath(__file__)).split("/")) + "/cputicks/")
import instructions
import mmu
import interupt
import debug
import time

class states():
	OPCODE = 1
	EXT_OPCODE = 2
	OPERAND = 3
	RUNNING = 4
	IRQ_READ_IF = 5
	IRQ_READ_IE = 6
	IRQ_PUSH_1 = 7 
	IRQ_PUSH_2 = 8
	IRQ_PUSH_2_AND_JUMP = 9
	STOPPED = 10
	HALTED = 11


class cpu(object):
	def __init__(self, gui, refrence, interruptManager):

		self.register = cpuhelper.register()
		self.interruptManager = interruptManager
		
		import serial
		self.serial = serial.serial()
		self.adressSpace = mmu.Mmu(gui, self.interruptManager, refrence, self.serial)


		self.state = states.OPCODE

		self.debuger = debug.debug(self.register, self.adressSpace)
		self.debuger.giveOpcodes(instructions.opcodes + instructions.extOpcodes)

		'''
		self.register.AF = 0x0100
		self.register.BC = 0x0013
		self.register.DE = 0x00d8
		self.register.HL = 0x014d

		self.register.SP = 0xfffe
		self.register.PC = 0x0100

		self.register.localflags.setZ(True)
		self.register.localflags.setH(True)
		self.register.localflags.setC(True)
		'''

		#AF=0100, BC=0013, DE=00d8, HL=014d, SP=fffe, PC=0100, Z-HC----

	opcodeArgs = [0x0] * 2
	opcode1 = None
	opcode2 = None
	currentOpcode = None


	interruptFlag = 0
	interruptEnabled = 0

	rounds = 0

	opIndex = 0
	opContext = 0
	operandIndex = 0
	roundx = 0
	requestedIrq = None
	totalrounds = 0


	realtalk = 0
	orginalpc = 0
	def ticktest(self):

		def clearstate():
			self.opcode1 = 0
			self.opcode2 = 0
			self.currentOpcode = None

			self.opcodeArgs = [0x0] * 2
			self.operandIndex = 0

			self.opIndex = 0
			self.opContext = 0

			self.interruptFlag = 0
			self.interruptEnabled = 0
			self.requestedIrq = None

			
		if(self.state == states.OPCODE or self.state == states.HALTED or self.state == states.STOPPED):
			if(self.interruptManager.isInterruptRequested()):
				self.state = states.IRQ_READ_IF

		if(self.state == states.HALTED):
			if(self.interruptManager.isInterruptFlagSet()):
				self.state = states.OPCODE

		if(self.serial.EnableBlattsDebug):
			if(self.register.getBC() == 4608 or
				self.register.getBC() ==  1200):
				self.register.debug = True
			if(self.register.debug):
				self.debuger.trace(self.currentOpcode)
				time.sleep(1)

	#	self.nommulrodsun += 1
		pc = self.register.getPC()


		if(self.state == states.OPCODE):
			clearstate()
			self.opcode1 = self.adressSpace.getByte(pc)
			if((self.opcode1) == 0xcb):
				self.state = states.EXT_OPCODE

			elif((self.opcode1) == 0x10):
				self.currentOpcode = instructions.opcodes[self.opcode1]
				
			else:
				self.state = states.OPERAND
				self.currentOpcode = instructions.opcodes[self.opcode1]
				self.orginalpc = pc
				
				
				if(self.currentOpcode == None):
					raise Exception("Bad opcode in currentopcode ")

			self.register.incrementPC()
			return

		elif(self.state == states.EXT_OPCODE):
			self.opcode2 = self.adressSpace.getByte(pc)

			if(self.currentOpcode == None):
				self.currentOpcode = instructions.extOpcodes[self.opcode2]
				
				
			if(self.currentOpcode == None):
				raise Exception("Bad opcode ext")
			
			self.state = states.OPERAND
			self.register.incrementPC()
			return
		elif(self.state == states.OPERAND):

			if(self.operandIndex < self.currentOpcode.argstotal()):
				self.opcodeArgs[self.operandIndex] = self.adressSpace.getByte(pc)

				self.register.incrementPC()
				self.operandIndex += 1
				return

			self.state = states.RUNNING

		if(self.state == states.RUNNING):
			if(self.opcode1 == 0x10):
				self.state = states.STOPPED
				return
			elif(self.opcode1 == 0x76):
				self.state = states.HALTED
				return


			self.debuger.checkBreakpoint(hex(self.currentOpcode.opcode), self.currentOpcode.label)
			while self.opIndex < len(self.currentOpcode.instructions):
				currnetOP = self.currentOpcode.instructions[self.opIndex]
				self.opContext = currnetOP.execute(self.register, self.adressSpace, self.opcodeArgs, self.opContext)
				currnetOP.switchInterrupts(self.interruptManager)

				self.opIndex += 1

				if not currnetOP.prooced(self.register):
					self.opIndex = len(self.currentOpcode.instructions)
					break
				if(currnetOP.readMemory or currnetOP.writeMemory):
					break


			if(self.opIndex >= len(self.currentOpcode.instructions)):
				self.state = states.OPCODE
				self.operandIndex = 0		
				self.debuger.tick(self.currentOpcode.label)
				self.interruptManager.onInstructionFinished()
			return 
		if(self.state == states.IRQ_READ_IF):
			self.interruptFlag = self.adressSpace.getByte(0xff0f)
			self.state = states.IRQ_READ_IE
			return

		if(	self.state == states.IRQ_READ_IE):
			self.interruptEnabled = self.adressSpace.getByte(0xffff)
			self.requestedIrq = None

			for irq in range(0, len(self.interruptManager.respone.values())):
				if ((self.interruptFlag & self.interruptEnabled & (1 << irq)) != 0) :
					self.requestedIrq = self.interruptManager.respone.values()[irq]
					break
	
			self.interruptManager.flush()
			if(self.requestedIrq == None):
				self.state = states.OPCODE
			else:
				self.state = states.IRQ_PUSH_1
				self.interruptManager.disableInterrupts(False)
			return

		if(self.state == states.IRQ_PUSH_1):
			self.register.decrementSP()
			self.adressSpace.setByte(self.register.getSP(), (self.register.getPC() & 0xff00) >> 8);
			self.state = states.IRQ_PUSH_2_AND_JUMP;
			return

		if(self.state == states.IRQ_PUSH_2_AND_JUMP):
			self.register.decrementSP()
			self.adressSpace.setByte(self.register.getSP(), self.register.getPC() & 0x00ff);

			#raise Exception("BUG")
			self.register.setPC(self.requestedIrq);
			self.requestedIrq = None

			self.state = states.OPCODE

			return











