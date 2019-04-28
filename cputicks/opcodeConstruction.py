

import arguments
import alu

class create:

	lastDataType = None

	def __init__(self, opcode, label):
		self.instructions = []
		self.opcode = opcode
		self.label = label
		
	def argstotal(self):
		arsgslen = [0]
		for x in self.instructions:
			arsgslen.append(x.argsLength)
		return max(arsgslen)

	def copyByte(self, target, source):

		self.load(source)
		self.store(target)
		return self

	def load(self, source):
		import instructions
		loadArg = arguments.parse(source)

		self.lastDataType  = loadArg.datatype


		self.instructions.append(instructions.operation(read=loadArg.memory, length=loadArg.argslen, execution= lambda reg,adr,args,context : loadArg.read(reg,adr,args) ))
		return self

	def store(self, source):
		import instructions
		writeArg = arguments.parse(source)
		#print(self.lastDataType)
		if(writeArg.label in "(a16)" and "16bit" in self.lastDataType ):
#			print("GLAD :=()")	
			self.instructions.append(instructions.operation(write=writeArg.memory,length=writeArg.argslen, execution=lambda reg,adr,args,context : writeArg.write2(reg,adr,args, context,0) ) )
			self.instructions.append(instructions.operation(write=writeArg.memory,length=writeArg.argslen, execution=lambda reg,adr,args,context : writeArg.write2(reg,adr,args, context,1) ) )
		else:
			self.instructions.append(instructions.operation(write=writeArg.memory,length=writeArg.argslen, execution=lambda reg,adr,args,context : writeArg.write(reg,adr,args, context) ) )
		return self

	def switchInterrupts(self, enable, withDelay):
		import instructions
		if(enable):
			self.instructions.append(instructions.operation(switchInterrupts=lambda interruptManager:interruptManager.enableInterrupts(withDelay) ) )
		else:
			self.instructions.append(instructions.operation(switchInterrupts=lambda interruptManager:interruptManager.disableInterrupts(withDelay)  ) )
		return self



	def loadWord(self, value):
		import instructions
		self.lastDataType  = "16bit"

		self.instructions.append(instructions.operation(execution=lambda reg,adr,args,context : value ) )
		return self


	def proceedIf(self, value):
		import instructions
		
		def checkreg(register, value):
			if(value == "NZ"):
				return not register.localflags.isZ()
			elif(value == "Z"):
				return register.localflags.isZ()
			elif(value == "NC"):
				return not register.localflags.isC()
			elif(value == "C"):
				return register.localflags.isC()
			else:
				False

		self.instructions.append(instructions.operation(prooced=lambda register, value=value : checkreg(register, value), execution=lambda reg,adr,args,context : context ) )
		return self		

	def push(self):		
		import instructions
	
		def runcode(registers, addressSpace,context):
			registers.decrementSP()
			addressSpace.setByte(registers.getSP(), (context & 0xff00) >> 8)
			return context

		def runcode2(registers, addressSpace,context):
			registers.decrementSP()
			addressSpace.setByte(registers.getSP(), (context & 0x00ff))
			return context


		self.instructions.append(instructions.operation(write=True, execution=lambda reg,adr,args,context : runcode(reg, adr, context) ) )
		self.instructions.append(instructions.operation(write=True, execution=lambda reg,adr,args,context : runcode2(reg, adr, context) ) )
		return self
	def pop(self):
		import instructions
		self.lastDataType  = "16bit"

		def runcode(reg, addressSpace, context):
			lsb = addressSpace.getByte(reg.getSP())
			reg.incrementSP()
			return lsb

		def runcode2(reg, addressSpace, context):
			msb = addressSpace.getByte(reg.getSP())
			reg.incrementSP()


			return context | (msb << 8)
		

		self.instructions.append(instructions.operation(read=True, execution=lambda reg,adr,args,context : runcode(reg, adr, context) ) )
		self.instructions.append(instructions.operation(read=True, execution=lambda reg,adr,args,context : runcode2(reg, adr, context) ) )
		return self

	def alu(self, operation, value=None):
		import instructions
		
		if(type(value) == str):
			def runcode(reg,adr,args,context,arg2s,func):
				v2 = arg2s.read(reg,adr,args)
				return func(reg.localflags, context, v2)

			arg = arguments.parse(value)
			func = alu.find(operation, self.lastDataType, arg.datatype)
			#print(func)
			self.instructions.append(instructions.operation(read=arg.memory,length=arg.argslen, execution=lambda reg,adr,args,context,arg2=arg,fu=func : runcode(reg, adr, args,context,arg2,fu) ) )
		elif(type(value) == int):
			func = alu.find(operation, self.lastDataType, "8bit")
			self.instructions.append(instructions.operation(execution=lambda reg,adr,args,context,val =value : func(reg.localflags, context, val) ) )
		else:
			func = alu.find(operation, self.lastDataType)
			self.instructions.append(instructions.operation(execution=lambda reg,adr,args,context: func(reg.localflags, context) ) )
		return self		
