


class cartridgeTypes:
	types = {
				"ROM ": 0x00,
				"ROM_MBC1 ": 0x01,
				"ROM_MBC1_RAM ": 0x02,
				"ROM_MBC1_RAM_BATTERY ": 0x03,
				"ROM_MBC2 ": 0x05,
				"ROM_MBC2_BATTERY ": 0x06,
				"ROM_RAM ": 0x08,
				"ROM_RAM_BATTERY ": 0x09,
				"ROM_MMM01 ": 0x0b,
				"ROM_MMM01_SRAM ": 0x0c,
				"ROM_MMM01_SRAM_BATTERY ": 0x0d,
				"ROM_MBC3_TIMER_BATTERY ": 0x0f,
				"ROM_MBC3_TIMER_RAM_BATTERY ": 0x10,
				"ROM_MBC3 ": 0x11,
				"ROM_MBC3_RAM ": 0x12,
				"ROM_MBC3_RAM_BATTERY ": 0x13,
				"ROM_MBC5 ": 0x19,
				"ROM_MBC5_RAM ": 0x1a,
				"ROM_MBC5_RAM_BATTERY ": 0x01b,
				"ROM_MBC5_RUMBLE ": 0x1c,
				"ROM_MBC5_RUMBLE_SRAM ": 0x1d,
				"ROM_MBC5_RUMBLE_SRAM_BATTERY ": 0x1e
			}
	gotID = None
	def getById(self, Typeid):
		self.gotID = self.types.keys()[self.types.values().index(Typeid)]
		return self.gotID

	def isType(self, typeName):
		return  typeName in self.types.keys()[self.types.values().index(Typeid)]

	def getRomBanks(self, romid):
		if(romid == 0):
			return 2
		elif(romid == 1):
			return 4
		elif(romid == 2):
			return 8
		elif(romid == 3):
			return 16
		elif(romid == 4):
			return 32
		elif(romid == 5):
			return 64
		elif(romid == 6):
			return 128
		elif(romid == 0x52):
			return 72
		elif(romid == 0x53):
			return 80
		elif(romid == 0x54):
			return 96	
		else:
			raise Exception("Bug . defiently")

	def getRamBanks(self, ramid):
		if(ramid == 0):
			return 0
		elif(ramid == 1):
			return 1
		elif(ramid == 2):
			return 1
		elif(ramid == 3):
			return 4
		elif(ramid == 4):
			return 16
		else:
			raise Exception("Bug defiently")







