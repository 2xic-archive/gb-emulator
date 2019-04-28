



class Lcdc:
	lcdc = 0


	def isBgAndWindowDisplay(self):
		return (self.lcdc & (1 << 0)) != 0

	def isObjDisplay(self):
		return (self.lcdc & (1 << 1)) != 0

	def getSpriteHeight(self):
		return (8 if(self.lcdc & (1 << 2)) == 0 else 16 ) 

	def getBgTileMapDisplay(self):
		return 0x9800 if( (self.lcdc & (1 << 3)) == 0) else 0x9c00

	def getBgWindowTileData(self):
		return (0x9000 if(self.lcdc & (1 << 4)) == 0  else 0x8000)

	def isBgWindowTileDataSigned(self):
		return (self.lcdc & (1 << 4)) == 0

	def isWindowDisplay(self):
		return (self.lcdc & (1 << 5)) != 0

	def getWindowTileMapDisplay(self):
		return (0x9800 if(self.lcdc & (1 << 6)) == 0 else 0x9c00)

	def isLcdEnabled(self):
		return (self.lcdc & (1 << 7)) != 0