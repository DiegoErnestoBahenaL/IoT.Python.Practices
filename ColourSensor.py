import RPi.GPIO as GPIO
import time

# Set up GPIO pin numbering mode
GPIO.setmode(GPIO.BCM)

S3_PIN = 17
S2_PIN = 27
OUT_PIN = 22

GPIO.setup(S2_PIN, GPIO.OUT)
GPIO.setup(S3_PIN, GPIO.OUT)
GPIO.setup(OUT_PIN, GPIO.IN)



def calibrate_red():
    GPIO.output(S2_PIN, False)
    GPIO.output(S3_PIN, False)

def calibrate_blue():
    GPIO.output(S2_PIN, False)
    GPIO.output(S3_PIN, True)

try:

    calibrate_blue()

    while True:

        if (GPIO.input(OUT_PIN)):
            print("Color azul detectado!")   

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Programa terminado por el usario.")
finally:
    GPIO.cleanup() # Clean up GPIO settings on exit     