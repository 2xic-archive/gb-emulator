



class Spriteflags:

	def __init__(self,flags):
		self.flags = flags

	def isPriority(self):
		return (self.flags & (1 << 7)) != 0;

	def isYflip(self):
		return (self.flags & (1 << 6)) != 0;

	def isXflip(self):
		return (self.flags & (1 << 5)) != 0;

	def getPalette(self, OBP0, OBP1):
		return OBP0 if(self.flags & (1 << 4)) else OBP1
		