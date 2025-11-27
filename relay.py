import RPi.GPIO as GPIO
import time

# Set up GPIO pin numbering mode
GPIO.setmode(GPIO.BCM)

RELAY_PIN = 14

GPIO.setup(RELAY_PIN, GPIO.OUT)


try:

    output = True

    while True:

        GPIO.output(RELAY_PIN, output)
        output = not output
        
        time.sleep(1.5)

except KeyboardInterrupt:
    print("Programa termiinado por el usario.")
finally:
    GPIO.cleanup() # Clean up GPIO settings on exit        
