
import phase as allphase
import lcdc as lcdcimport

class gpu():
	VHBlank = 0
	VVBlank = 1
	VOamSearch = 2
	VPixelTransfer = 3


	scrollX = 0
	scrollY = 0
	stat = 0

	lcdc = lcdcimport.Lcdc()
#	line = 0
	ly = 0
	lyc = 0	
	WX = 0
	WY = 0
	BGP = 0
	OBP0 = 0
	OBP1 = 0
	

	ticksInLine = 0

	totalrounds = 0
	
	hyperdebug = False
	
	def __init__(self, ram, guiConnecrion, impManger):

		self.interruptManager = impManger


		self.ram = ram

		self.phase = allphase.OamSearch(self.ram, self, self.lcdc)
		self.mode = self.VOamSearch
		self.displaywindow = guiConnecrion._screenBuffer
	

	def setpixel(self, x, y, colo):
		import sdl2
		if(colo == 255):
			self.displaywindow.set((y,x), sdl2.ext.Color(r=colo,g=colo,b=colo))#, a=0))
		else:
			self.displaywindow.set((y,x), sdl2.ext.Color(r=colo,g=colo,b=colo, a=0))
			

	def dumpVideoRma(self):
		mapd = 0x9800 if((self.lcdc.lcdc & (1 << 3)) == 0)  else 0x9c00
		#	addres , offset, lengt, width
		offset = mapd
		length = 32 * 32
		width = 32

		z = []
		for i in range(offset, offset + length):
			if((i - offset + 1) % width):
				pass
			z.append(str(self.ram.getByte(i)))
		print(",".join(z))


	def tick(self):
		screenRefreshed = False
		phaseprogress = self.phase.tick()

		self.ticksInLine += 1


		if(phaseprogress):
			if(self.mode == self.VHBlank):
				if (self.lcdc.isLcdEnabled()):
					#self.displaywindow.enableLcd()
					pass
				else:
					#self.displaywindow.disableLcd()
					pass
			
		else:
			if(self.mode == self.VOamSearch):
				self.mode = self.VPixelTransfer

				self.phase = allphase.makepixel(self.ly, self.ram, self.lcdc.lcdc, self.scrollX, self.scrollY, self, self.phase.getSprites(), self)#, self.data, self)
				return screenRefreshed

				#	some more code ???
			elif(self.mode == self.VPixelTransfer):
				self.mode = self.VHBlank
				self.phase = allphase.HBlankPhase(self, self.ticksInLine)
				self.requestLcdcInterrupt(3)
				return screenRefreshed

			elif(self.mode == self.VHBlank):
				self.ticksInLine = 0
				self.ly += 1
				if(self.ly == 144):	#	mad width
					self.mode = self.VVBlank
					self.phase = allphase.VBlankPhase(self)
					self.interruptManager.requestInterrupt(self.interruptManager.get("VBlank"))
					self.requestLcdcInterrupt(4)

				else:
					self.mode = self.VOamSearch
					self.phase = allphase.OamSearch(self.ram, self, self.lcdc)
					self.requestLcdcInterrupt(5)
				self.requestLycEqualsLyInterrupt()
				return screenRefreshed

			elif(self.mode == self.VVBlank):
				self.ticksInLine = 0
				self.ly += 1
				if(self.ly == 154):	#	max heigth
					self.mode = self.VOamSearch
					self.ly = 0
					self.phase = allphase.OamSearch(self.ram, self, self.lcdc)
					self.requestLcdcInterrupt(5)
					screenRefreshed = True
				else:
					self.phase = allphase.VBlankPhase(self)
				self.requestLycEqualsLyInterrupt()
				self.totalrounds += 1
		return screenRefreshed

	def requestLcdcInterrupt(self, statBit):
		if ((self.stat & (1 << statBit)) != 0):
			self.interruptManager.requestInterrupt(self.interruptManager.get("LCDC"))

	def requestLycEqualsLyInterrupt(self):
		if(self.ly == self.lyc):
			self.requestLcdcInterrupt(6)

	def getStat(self):
		return (self.stat | self.mode | ((1 << 2) if(self.ly == self.lyc) else 0))


	#	thank you http://imrannazar.com/GameBoy-Emulation-in-JavaScript:-Integration
	def handler(self, memory):
	#	0x8000, 0x2000		videoram...
		if(memory >= 0x8000 and memory < (0x8000 + 0x2000)):
			return self.ram.getByte(memory)
		elif(memory >= 0xfe00 and memory < (0xfe00 + 0x00a0)):
			return self.ram.getByte(memory)
		else:
			if(memory == 0xff40):
				return self.lcdc.lcdc
			elif(memory == 0xff41):
				return self.getStat()
			elif(memory == 0xff42):
				return self.scrollY
			elif(memory == 0xff43):
				return self.scrollX
			elif(memory == 0xff45):
				return self.lyc
			elif(memory == 0xff44):
				return self.ly
			elif(memory == 0xff47):
				return self.BGP
			elif(memory == 0xff48):
				return self.OBP0
			elif(memory == 0xff49):
				return self.OBP1
			elif(memory == 0xff4a):
				return self.WX
			elif(memory == 0xff4b):
				return self.WY
		return 0xff

	def setByte(self, address, value):	
		if(address >= 0x8000 and address < (0x8000 + 0x2000)):
			self.ram.setByte(address, value)
		elif(address >= 0xfe00 and address < (0xfe00 + 0x00a0)):
			self.ram.setByte(address, value)
		else:
			if(address == 0xff40):
				self.lcdc.lcdc = value
			if(address == 0xff41):
				self.stat = value & 0b11111000			
			elif(address == 0xff42):
				self.scrollY = value
			elif(address == 0xff43):
				self.scrollX = value
			elif(address == 0xff45):
				self.lyc = value
			elif(address == 0xff44):
				raise Exception("Should nto set variable ly?")
			elif(address == 0xff47):
				self.BGP = value
			elif(address == 0xff48):
				self.OBP0 = value
			elif(address == 0xff49):
				self.OBP1 = value
			elif(address == 0xff4a):
				self.WX = value
			elif(address == 0xff4b):
				self.WY = value

	def validadress(self, address):
		if(address >= 0x8000 and address < (0x8000 + 0x2000)):
			return True #)
		elif(address >= 0xfe00 and address < (0xfe00 + 0x00a0)):
			return True #)
		else:
			if(address == 0xff40):
				return True #
			if(address == 0xff41):
				return True #
			elif(address == 0xff42):
				return True #
			elif(address == 0xff43):
				return True #
			elif(address == 0xff45):
				return True #
			elif(address == 0xff44):
				return True
			elif(address == 0xff47):
				return True #
			elif(address == 0xff48):
				return True #
			elif(address == 0xff49):
				return True #
			elif(address == 0xff4a):
				return True #
			elif(address == 0xff4b):
				return True #value



	def getByte(self, address):
		return self.handler(address)







