import RPi.GPIO as GPIO
import time

# Set up GPIO pin numbering mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the sensor's digital output
HUMIDITY_SENSOR_PIN = 14  # Adjust this to your chosen GPIO pin

# Set up the GPIO pin as an input with a pull-down resistor
GPIO.setup(HUMIDITY_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def detect_humidity():
    """Reads the digital output of the sound sensor and prints its status."""
    humidity_detected = GPIO.input(HUMIDITY_SENSOR_PIN)  # Read the digital signal
    if humidity_detected == 1:
        print("Sonido detectado.")
     

try:
    print("Ajusta el potenciometro en el sensor de humedad para afinar su sensibilidad.")

    while True:
        detect_humidity()  # Check sound sensor status
        time.sleep(0.1) 
        
except KeyboardInterrupt:
    print("Programa termiinado por el usario.")
finally:
    GPIO.cleanup() # Clean up GPIO settings on exit
