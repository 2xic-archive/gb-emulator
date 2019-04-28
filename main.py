import sys
import time
import sdl2
import sdl2.ext
import numpy as np
import warnings
from abc import abstractmethod
import cpu
import os
sys.path.append("/".join(os.path.dirname(os.path.realpath(__file__)).split("/")) + "/gpu/")

import gpu
import interupt
import signal
import threading
from os import path
import sdl2.sdlmixer
from sdl2.sdlmixer import Mix_QuickLoad_RAW, Mix_PlayChannel, Mix_Playing, Mix_VolumeChunk
import ctypes
from sdl2 import *
from sdl2.sdlmixer import *
import random
from ctypes import *
from sdl2 import Sint16




gameboyResolution = (160*2, 144*2) 
thread = None
controller_ref = None
update_screen = False

class frame_buffer():
	def __init__(self, array):
		self._array = array
		self.enabled = True

	def fill(self, val):
		self._array.fill(val)

	def set(self, key, item):
		if not self.enabled:
			self.fill(sdl2.ext.Color(r=0,g=0,b=0))

		self._array[key] = item
	
	def enableLcd(self):
		self.enabled = True

	def disableLcd(self):
		self.enabled = False

def pixels2dWithoutWarning(surface):
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		return sdl2.ext.pixels2d(surface)

def keyPress(keyid, unpressed=False):
	function = controller_ref.buttonPress
	if(unpressed):
		function = controller_ref.buttonUnPress

	if(keyid == sdl2.SDLK_UP):
		function("UP")
	if(keyid == sdl2.SDLK_DOWN):
		function("DOWN")
	if(keyid == sdl2.SDLK_RIGHT):
		function("RIGHT")
	if(keyid == sdl2.SDLK_LEFT):
		function("LEFT")
	if(keyid == sdl2.SDLK_a):
		function("A")
	if(keyid == sdl2.SDLK_b):
		function("B")
	if(keyid == sdl2.SDLK_z):
		function("START")
	if(keyid == sdl2.SDLK_x):
		function("SELECT")

class SdlAudioManager():
	def addBuffer(self, source):
		audio_frequency = (1.0 * 200 / self.have.freq)
		length = len(source)# want.samples * want.channels
		data = (ctypes.c_int16 * (length))()

		for i in range(length):
			data[i] = source[i]
		SDL_QueueAudio(self.device, data, ctypes.sizeof(data))


	def __init__(self):
		self.audio_position = 0

		SDL_AudioCallback = CFUNCTYPE(None, c_void_p, POINTER(Uint8), c_int)
		SDL_Init(SDL_INIT_AUDIO)# | SDL_INIT_TIMER)
		want = SDL_AudioSpec(freq=44100,
				aformat=AUDIO_S16,
				channels=1,
				samples=44100
		)
		SDL_memset(ctypes.addressof(want), 0, ctypes.sizeof(want))
		self.have = SDL_AudioSpec(freq=44100,
				aformat=AUDIO_S16,
				channels=1,
				samples=44100
		)
		self.audio_frequency = 1.0 * 200 / self.have.freq

		self.device = SDL_OpenAudioDevice(None, 0, want, self.have, SDL_AUDIO_ALLOW_FORMAT_CHANGE)
		if(self.device == 0):
			print("Feil {}".format(SDL_GetError()))
			exit(0)
		

		SDL_PauseAudioDevice(self.device, 0)



class SdlGameWindow():
	def __init__(self, scale=3):

		global thread
		global update_screen
		sdl2.ext.init()


		self.audio = SdlAudioManager()

		self._window = sdl2.ext.Window("gb", size=gameboyResolution)
		self._windowSurface = self._window.get_surface()

		self._screenBuffer = frame_buffer(pixels2dWithoutWarning(self._windowSurface))
		self._screenBuffer.fill(0x00558822)
		self._window.show()
		self.updateDisplay()
		
		thread = threading.Thread(target=worker, args=(self,))
		thread.deamon = True
		try:
			thread.start()
			
			while thread.isAlive():     
				if(update_screen):
					self.updateDisplay()
					self._screenBuffer.oppdatert = False

				for e in sdl2.ext.get_events():
					if e.type == sdl2.SDL_QUIT:
						running = False
						break
					if e.type == sdl2.SDL_KEYDOWN:
						if e.key.keysym.sym == sdl2.SDLK_ESCAPE:
							running = False
							break
						elif(controller_ref != None):
							keyPress(e.key.keysym.sym)

					if e.type == sdl2.SDL_KEYUP and controller_ref != None:
						keyPress(e.key.keysym.sym, True)
				time.sleep(0.01)
		except Exception as e:
			exit_gracefully()

	def updateDisplay(self):
		self._window.refresh()


import cartridge

_FINISH = False
def worker(screen):
	def loadmario():
		print(cpulogic.adressSpace.rom)

		readROM = []
		filename = ""
		if(len(filename) == 0):
			print("need to set filename variable in main.py")
			exit(0)
		romFile = open(filename, "rb").read()

		for x in romFile:
			readROM.append( (ord(x) & 0xff))

		cpulogic.adressSpace.rom.type = cartridge.cartridgeTypes().getById(ord(romFile[0x0147]))
		cpulogic.adressSpace.rom.romBanks = cartridge.cartridgeTypes().getRomBanks(ord(romFile[0x0148]))
		cpulogic.adressSpace.rom.ramBanks = cartridge.cartridgeTypes().getRamBanks(ord(romFile[0x0149]))

		Name = ""
		for i in range(0x0134, 0x0143):
			Name += (chr(int(ord(romFile[i]))))
		print("Loaded game {}".format(Name))

		cpulogic.adressSpace.rom.space = readROM
		cpulogic.adressSpace.rom.offset = 0
		cpulogic.adressSpace.rom.custom = True
		import mmu
		cpulogic.adressSpace.rom.cartRidgeRam =  mmu.generateRam(0x2000)

	import interupt
	global _FINISH
	global controller_ref
	global update_screen
	import controllers
	

	interruptManager = interupt.interupttype()

	controller_ref = controllers.joycontrollers(interruptManager)

	cpulogic = cpu.cpu(screen, controller_ref, interruptManager)#,interruptManager)
	loadmario()
	cputick = 0
	while not _FINISH:  
		if(cputick == 0):
			cpulogic.ticktest()
	
		cputick = (cputick + 1) % 4
		cpulogic.adressSpace.timer.tick()
		
		cpulogic.adressSpace.dma.tick()
		

		oppdateraa = cpulogic.adressSpace.gpu.tick()
		if(oppdateraa):
			update_screen = True
		
		

def exit_gracefully():
	signal.signal(signal.SIGINT, original_sigint)
	global _FINISH
	_FINISH = True
	while thread.isAlive():
		time.sleep(1)
	exit(0)

	signal.signal(signal.SIGINT, exit_gracefully)

original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)


widnow = SdlGameWindow()







