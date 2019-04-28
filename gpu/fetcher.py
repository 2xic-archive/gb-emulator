


import sprites
class states:
	READ_TILE_ID = 0
	READ_DATA_1 = 1
	READ_DATA_2 = 2
	PUSH = 3

	READ_SPRITE_TILE_ID = 4
	READ_SPRITE_FLAGS = 5
	READ_SPRITE_DATA_1 = 6
	READ_SPRITE_DATA_2 = 7
	PUSH_SPRITE = 8


class fetcher:

	xpos = 0
	divider = False
	state = states.READ_TILE_ID
	tileId = 0
	tileData1 = 0
	tileData2 = 0


	spriteTileLine = 0
	sprite = None
	spriteFlags = None
	mapAddress = 0


	debug = False

	VfetchingDisabled = False
	def __init__(self, fifo, line, videoram, lcdc, scrollx, scrolly, debug=False):
		self.fifo = fifo
		self.videoram = videoram
		self.line = line

#		self.scrollx = scrollx
#		self.scrolly = scrolly
		self.lcdc = lcdc
		self.debug = debug

	def startFetching(self, mapAddress, tileDataAddress, tileIdSigned, tileLine):
		self.mapAddress = mapAddress
		self.tileDataAddress = tileDataAddress
		self.tileIdSigned = tileIdSigned
		self.tileLine = tileLine

		self.state = states.READ_TILE_ID
		self.divider = False
		self.tileId = 0
		self.tileData1 = 0
		self.tileData2 = 0

	
	def fetchingDisabled(self):
		self.VfetchingDisabled = True

	def addSprite(self, sprite):

		self.sprite = sprite
		self.state = states.READ_SPRITE_TILE_ID
		self.spriteTileLine = self.line.ly + 16 - sprite.getY();


	sum0 = 0
	sum1 = 0

	def tick(self):
		if(self.debug):
			print("Fetcher state == {} ".format(self.state))

		if(self.VfetchingDisabled and self.state == states.READ_TILE_ID):
			if(self.fifo.getLength() <= 8):
				self.sum1 += 1

				self.fifo.enquePixels(0, 0)
			return
		if(self.debug):
			print("FetchingDisabled")


		
		self.divider = not self.divider

		if not self.divider:
			return None

		if(self.debug):
			print("Divider")

		if(self.state == states.READ_TILE_ID):
			self.tileId = self.videoram.getByte(self.mapAddress)
			self.state = states.READ_DATA_1
			return

		if(self.state == states.READ_DATA_1):
			self.tileData1 = self.getTileData(self.tileId, self.tileLine, 0, self.tileDataAddress, self.tileIdSigned)
			self.state = states.READ_DATA_2
			return

		if(self.state == states.READ_DATA_2):
			self.tileData2 = self.getTileData(self.tileId, self.tileLine, 1, self.tileDataAddress, self.tileIdSigned)
			self.state = states.PUSH
		
		if(self.state == states.PUSH):
			if(self.fifo.getLength() <= 8):
				self.sum0 += 1
				self.fifo.enquePixels(self.tileData1, self.tileData2)
				
				self.state = states.READ_TILE_ID
				self.mapAddress += 1
			return

		if(self.state == states.READ_SPRITE_TILE_ID):
			self.tileId = self.videoram.getByte(self.sprite.getAddress() + 2)
			self.state = states.READ_SPRITE_FLAGS
			return

		if(self.state == states.READ_SPRITE_FLAGS):

			self.spriteFlags = sprites.Spriteflags( self.videoram.getByte(self.sprite.getAddress() + 3))
			if(self.spriteFlags.isYflip()):
				self.spriteTileLine = 15 - self.spriteTileLine
			self.state = states.READ_SPRITE_DATA_1
			return

		if(self.state == states.READ_SPRITE_DATA_1):
			self.tileData1 = self.getTileData(self.tileId, self.spriteTileLine, 0, 0x8000, False)
			self.tileData1adr = self.getTileDataAdreess(self.tileId, self.spriteTileLine, 0, 0x8000, False)
			self.state = states.READ_SPRITE_DATA_2
			return

		if(self.state == states.READ_SPRITE_DATA_2):
			self.tileData2 = self.getTileData(self.tileId, self.spriteTileLine, 1, 0x8000, False)
			self.tileData2adr = self.getTileDataAdreess(self.tileId, self.spriteTileLine, 1, 0x8000, False)
			self.state = states.PUSH_SPRITE
			return

		if(self.state == states.PUSH_SPRITE):
			self.fifo.setOverlay(self.tileData1, self.tileData2, 0, self.spriteFlags)
			self.state = states.READ_TILE_ID
			return

	def spriteInProgress(self):
		return self.state >= 4


	def isNegative(self, signedByteValue):
		return (signedByteValue & (1 << 7)) != 0;

	def abs(self, signedByteValue):
		if (self.isNegative(signedByteValue)):
			return 0x100 - signedByteValue;
		else:
			return signedByteValue;

	def getTileData(self, tileId, line, byteNumber, tileDataAddress, signed):
		tileAdress = None
		if(signed):
			if(self.isNegative(tileId)):
				tileAdress = tileDataAddress - abs(tileId) * 0x10
			else:
				tileAdress = tileDataAddress + abs(tileId) * 0x10
		else:
			tileAdress = tileDataAddress + tileId * 0x10
		return self.videoram.getByte(tileAdress + line * 2 + byteNumber)

	def getTileDataAdreess(self, tileId, line, byteNumber, tileDataAddress, signed):
		tileAdress = None
		if(signed):
			if(self.isNegative(tileId)):
				tileAdress = tileDataAddress - abs(tileId) * 0x10
			else:
				tileAdress = tileDataAddress + abs(tileId) * 0x10
		else:
			tileAdress = tileDataAddress + tileId * 0x10
		return (tileAdress + line * 2 + byteNumber)


	def dumpVideoRma(self):
		mapd = 0x9800 if((self.lcdc & (1 << 3)) == 0)  else 0x9c00
		#	addres , offset, lengt, width
		offset = mapd
		length = 32 * 32
		width = 32

		z = []
		for i in range(offset, offset + length):
			if((i - offset + 1) % width):
				pass
			z.append(str(self.videoram.getByte(i)))
		print(",".join(z))







