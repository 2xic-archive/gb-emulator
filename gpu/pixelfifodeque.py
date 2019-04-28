

import collections

class pixelfifo:
	
	overlayPalette = None


	def __init__(self, bgp, ob0, ob1):
		self.bgp = bgp
		self.ob0 = ob0
		self.ob1 = ob1

		self.deque = collections.deque([]) 
		self.overlaydeque = collections.deque([]) 
		self.overlayPriority = False

	def getLength(self):
		return len(self.deque)

	def dequeuePixel(self):
		if(len(self.overlaydeque) == 0):
#			print(0)
			return self.getBgColor(self.deque.popleft())
		else:
			self.overlaypixel = self.overlaydeque.popleft()
			self.pixel = self.deque.popleft()
			if(self.overlayPriority):
				return self.getObjectColor(self.overlaypixel) if(self.pixel == 0) else self.getBgColor(self.pixel)
			else:
				return self.getObjectColor(self.overlaypixel)
		
	def enquePixels(self, data1, data2):
		for i in self.zip(data1, data2):
			self.deque.append(i)
#		print(len(self.deque))

	def zip(self, data1, data2):
		pixelLine = []

		for  i in range(7, -1, -1):
			mask = (1 << i)
			data1Mask = 0 if(data1&mask == 0) else 1
			data2Mask = 0 if(data2&mask == 0) else 1
#			pixel = (2 * (data1Mask + data2Mask))
			pixel = (2 * data1Mask + data2Mask)

			pixelLine.append( pixel )
		return pixelLine

	def setOverlay(self, data1, data2, offset, spriteflags):
		pixelLine = self.zip(data1, data2)
		if(spriteflags.isXflip()):
			pixelLine = reverse(pixelLine)

		self.overlayPriority = spriteflags.isPriority()
		self.overlayPalette = spriteflags.getPalette(self.ob0, self.ob1)

		for x in (pixelLine):
			if(x != 0 and x != 3):
				pass


		self.overlaydeque = collections.deque(pixelLine[offset:8]) 

	def getBgColor(self, colorIndex):
		return self.getColor(self.bgp , colorIndex)

	def getObjectColor(self, colorIndex):
		return self.getColor(self.overlayPalette, colorIndex)

	def getColor(self, pallete, colorIndex):
		return 0b11 & (pallete >> (colorIndex * 2))


	def getvalue(self):
		return self.value





