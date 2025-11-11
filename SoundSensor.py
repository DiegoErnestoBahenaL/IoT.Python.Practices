import RPi.GPIO as GPIO
import time

# Set up GPIO pin numbering mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the sensor's digital output
SOUND_SENSOR_PIN = 4  # Adjust this to your chosen GPIO pin

# Set up the GPIO pin as an input with a pull-down resistor
GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def detect_sound():
    """Reads the digital output of the sound sensor and prints its status."""
    sound_detected = GPIO.input(SOUND_SENSOR_PIN)  # Read the digital signal
    if sound_detected == 1:
        print("Sound detected!")


# Main program loop
try:
    print("Adjust the potentiometer on your sound sensor to tune its sensitivity.")
    print("If you see only 'Sound detected!', decrease sensitivity by turning the potentiometer counter-clockwise.")
    print("If you see only 'No sound detected.', increase sensitivity by turning the potentiometer clockwise.")
    while True:
        detect_sound()  # Check sound sensor status
        time.sleep(0.1) # Small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    GPIO.cleanup() # Clean up GPIO settings on exit
