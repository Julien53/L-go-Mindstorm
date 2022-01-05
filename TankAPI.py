import os
import ev3_dc as ev3
from ev3_dc.ev3 import Battery
from gtts import gTTS
from platform import system as getOS

class Ev3Controller:

	# Global variables
	device = None
	MAC = "00:16:53:48:91:73"
	ALL_MOTORS = [15]
	FRONT_MOTORS = [ev3.PORT_C, ev3.PORT_D]
	BACK_MOTORS = [ev3.PORT_A, ev3.PORT_B]
	LEFT_SIDE_MOTORS = [ev3.PORT_A, ev3.PORT_C]
	RIGHT_SIDE_MOTORS = [ev3.PORT_B, ev3.PORT_D]
	LINUX = (False, True)[getOS() == 'Linux']

	#Connexion to the mindstorm controller
	def __init__(self, MAC=None):
		self.device = ev3.EV3(protocol=ev3.BLUETOOTH, host=(MAC, self.MAC)[MAC == None], sync_mode=ev3.SYNC)
		self.device.verbosity = 1

	#Start chosen motor for undefined period of time
	def Start(self, speed, motorlist):
		motors = 0
		for m in motorlist:
			motors += m
		
		opStart = b''.join((
			ev3.opOutput_Power,
			ev3.LCX(0),
			ev3.LCX(motors),
			ev3.LCX(speed),
			ev3.opOutput_Start,
			ev3.LCX(0),
			ev3.LCX(motors)
		))
		self.device.send_direct_cmd(opStart)

	#Stop chosen motor
	def stop(self, motorlist):
		motors = 0
		for m in motorlist:
			motors += m

		self.device.send_direct_cmd(
			b''.join((
				ev3.opOutput_Stop,
				ev3.LCX(0),
				ev3.LCX(motors),
				ev3.LCX(0)
			))
		)

	#Move foward if speed positive and backward if negative
	def Move(self, speed):
		self.Start(-speed, self.FRONT_MOTORS)
		self.Start(speed, self.BACK_MOTORS)

	#Stop all motors
	def StopAll(self):
		self.stop(self.ALL_MOTORS)

		
	#Turn slightly left
	def TurnLeft(self, speed):
		self.Start(speed, [self.RIGHT_SIDE_MOTORS[0]])
		self.Start(-speed, [self.RIGHT_SIDE_MOTORS[1]])    
	
	#Turn slightly right
	def TurnRight(self, speed):
		self.Start(speed, [self.LEFT_SIDE_MOTORS[0]])
		self.Start(-speed, [self.LEFT_SIDE_MOTORS[1]])

	#Turn right on himself
	def TurnRightOnHimself(self, speed):
		self.TurnRight(speed)
		self.TurnLeft(-speed)

	#Turn left on himself
	def TurnLeftOnHimself(self, speed):
		self.TurnLeft(speed)
		self.TurnRight(-speed)
	
	def Stream(self):
		if (self.LINUX):
			os.system("sudo ffmpeg -ar 8000 -f alsa -i plughw:CARD=StudioTM -crf 1 -filter:a \"volume=1\" -preset veryfast -acodec mp3 -f hls -segment_time 1 -hls_time 1 -hls_playlist_type event '/var/www/html/stream/stream.m3u8' & disown")
		else:
			print("Only available in linux")
		

	#Make a built-in sound
	def Sound(self, which):
		hugo = ev3.Sound(protocol=ev3.BLUETOOTH, ev3_obj=self.device, volume=100)
		hugo.play_sound('../prjs/Project/' + which)
	
	#Say custom text
	def Speak(self, text, language='en'):
		if (self.LINUX):
			gTTS(text, lang=language).save('./sound/sound.mp3')
			os.system("./sound/ffmpeg -y -i ./sound/sound.mp3 -vn -acodec pcm_u8 -f u8 -ar 8000 -filter:a \"volume=2\" ./sound/sound.raw")
			os.system("./sound/raw2rsf ./sound/sound.raw > ./sound/sound.rsf")

			hugo = ev3.Sound(protocol=ev3.BLUETOOTH, ev3_obj=self.device, volume=100)

			hugo.play_sound('./sound/sound.rsf', local=True)
		else:
			print("Only available in linux")

	def GetBattery(self):
		battery = self.device.battery
		return battery.percentage