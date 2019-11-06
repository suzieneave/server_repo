from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
for i in range (10):
	sleep(3)
	camera.capture('/home/pi/Documents/images/image%s.jpg' % i)
camera.stop_preview()

