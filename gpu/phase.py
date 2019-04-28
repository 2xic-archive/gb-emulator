

#	http://www.codeslinger.co.uk/pages/projects/gameboy/graphics.html
#	http://imrannazar.com/GameBoy-Emulation-in-JavaScript:-Graphics

import lcdc

class SpritePosition:
	def __init__(self, x, y, adress):
		self.x = x
		self.y = y
		self.adress = adress

	def getX(self):
		return self.x

	def getY(self):
		return self.y
	
	def getAddress(self):
		return self.adress
	

class OamSearch:
	def __init__(self, ram, lyx, lcdc):
		self.oemRam = ram
		
		self.ly = lyx
		self.lcdc = lcdc 
		self.ticks = 0
		self.sprites = [None] * 10


	i = 0
	READING_Y = 0
	READING_X = 1
	spritePosIndex = 0
	
	states = READING_Y

	def tick(self):
		spriteaddress = 0xfe00 + 4 * self.i

		if(self.states == self.READING_Y):
			self.spriteY = self.oemRam.getByte(spriteaddress)
			self.states = self.READING_X
		elif(self.states == self.READING_X):
			self.spriteX = self.oemRam.getByte(spriteaddress+1)
			
			if(self.between(self.spriteY, self.ly.ly + 16, self.spriteY + self.lcdc.getSpriteHeight())):
				self.sprites[self.spritePosIndex] = SpritePosition(self.spriteX, self.spriteY, spriteaddress)
				self.spritePosIndex += 1

			self.states = self.READING_Y
			self.i += 1
			self.ticks += 1

		return self.i < 40

	def getSprites(self):
		return self.sprites


	def between(self, fromval, x , to):
		return fromval <= x and x < to


class HBlankPhase:
	def __init__(self, line, ticksinline):
		self.line = line
		self.ticks = ticksinline

	def tick(self):
		self.ticks += 1
		return self.ticks < 456

class VBlankPhase:
	def __init__(self, line):
		self.line = line
		self.ticks = 0

	def tick(self):
		self.ticks += 1
		return self.ticks < 456


class makepixel:
	pixels = 0
	scrolly = 0
	ticks = 0
	def __init__(self, line, videoRam, lcdc, scrollx, scrolly, refclass,sprites, gpu):
		import pixelfifodeque as pixelfifo
		import fetcher
		self.ly = refclass

		self.fifo = pixelfifo.pixelfifo(gpu.BGP, gpu.OBP0, gpu.OBP1)

		self.fetcher = fetcher.fetcher(self.fifo, self.ly, videoRam, lcdc, scrollx, scrolly, refclass.hyperdebug)


		self.scrolly = scrolly
		self.scrollx = scrollx

		self.lcdc = refclass.lcdc

		self.sprites = sprites

		if(self.lcdc.isBgAndWindowDisplay()):
			self.startFetchingBackground()
		else:
			self.fetcher.fetchingDisabled()

		self.gpuclass = refclass
		self.WX = self.gpuclass.WX
		self.WY = self.gpuclass.WY	

		self.debug = refclass

	
	droppedPixels = 0
	x = 0

	def tick(self):
		self.fetcher.tick()

		if(self.lcdc.isBgAndWindowDisplay()):
			if(self.fifo.getLength() <= 8):
				return True
			if(self.droppedPixels < (self.scrollx % 8) ):
				self.fifo.dequeuePixel()
				self.droppedPixels +=1
				return True
			if(self.lcdc.isWindowDisplay() and self.ly.ly >= self.WY and self.x == self.WX-7):
				self.startFetchingWindow()			


		dark = [
			255,	#	white
			170,	#	LIGHT_GRAY
			85,		#	DARK_GRAY
			0		#	BLACK
		]

		if(self.lcdc.isObjDisplay()):
			if(self.fetcher.spriteInProgress()):
				return True

			spriteAdded = False
			for indexSprite in range(0, len(self.sprites)):				
				if(self.sprites[indexSprite] == None):
					continue

				if(self.sprites[indexSprite].getX() - 8 == self.x):
					if not spriteAdded:
						self.fetcher.addSprite(self.sprites[indexSprite])
						spriteAdded = True
					self.sprites[indexSprite] = None
				if(spriteAdded):
					return True


		scale = 2
		color = self.fifo.dequeuePixel()
		for i in range(0, 2):
			for j in range(0, 2):
				self.gpuclass.setpixel(self.ly.ly * scale + i, self.x * scale + j, (dark[color]))

		self.x += 1
		self.ticks = self.x
		if(self.x == 160):
			return False
		return True

	def startFetchingBackground(self):
		bgX = self.scrollx
		bgY = (self.scrolly + self.ly.ly) % 0x100

		self.fetcher.startFetching(self.lcdc.getBgTileMapDisplay() + bgX / 0x08 + (bgY / 0x08) * 0x20, self.lcdc.getBgWindowTileData(), self.lcdc.isBgWindowTileDataSigned(), bgY % 0x08);

	def startFetchingWindow(self):
		winX = self.x - self.WX + 7;
		winY = self.ly.ly - self.WY
		
		self.fetcher.startFetching(self.lcdc.getWindowTileMapDisplay() + winX / 0x08 + (winY / 0x08) * 0x20, self.lcdc.getBgWindowTileData(), self.lcdc.isBgWindowTileDataSigned(), winY % 0x08);

