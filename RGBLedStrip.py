import RPi.GPIO as GPIO
import time

# Set up GPIO pin numbering mode
GPIO.setmode(GPIO.BCM)

BLUE_PIN = 17
GREEN_PIN = 27
RED_PIN = 22


GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)


def turn_on():
    GPIO.output(RED_PIN, True)
    GPIO.output(GREEN_PIN, True)
    GPIO.output(BLUE_PIN, True)   

def turn_off():

    GPIO.output(RED_PIN, False)
    GPIO.output(GREEN_PIN, False)
    GPIO.output(BLUE_PIN, False)

def turn_red_on():
    GPIO.output(RED_PIN, True)

def turn_red_off():
    GPIO.output(RED_PIN, False)


def turn_green_on():
    GPIO.output(GREEN_PIN, True)

def turn_green_off():
    GPIO.output(GREEN_PIN, False)

def turn_blue_on():
    GPIO.output(BLUE_PIN, True)

def turn_blue_off():
    GPIO.output(BLUE_PIN, False)


try:

    while True:

        turn_off()
        time.sleep(1.5)

        turn_red_on()
        time.sleep(1.5)
        turn_red_off()

        turn_green_on()
        time.sleep(1.5)
        turn_green_off()

        turn_blue_on()
        time.sleep(1.5)
        turn_blue_off()

        turn_on()
        time.sleep(1.5)

except KeyboardInterrupt:
    print("Programa termiinado por el usario.")
finally:
    GPIO.cleanup() # Clean up GPIO settings on exit        


