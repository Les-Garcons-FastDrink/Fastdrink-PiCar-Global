import time
import RPi.GPIO as GPIO


def show_gpio():
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
	for i in range(26):
		GPIO.setup(i, GPIO.IN)
		
	try:
		while True :
			string = ""
			for y in range(26):
				string += f" pin {y} : {GPIO.input(y)} "
			print(string)
			time.sleep(1)
			
	except KeyboardInterrupt:
		GPIO.cleanup() # Clean up GPIO settings on exit




if __name__ == "__main__":
	show_gpio()
