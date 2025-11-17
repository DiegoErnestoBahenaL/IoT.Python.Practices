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
        print("Sonido detectado.")
     


try:
    print("Ajusta el potenciometro en el sensor de sonido para afinar su sensibilidad.")
    print("Si solo ves 'Sonido detectado.', disminuye la sensibilidad girando el potenciometro en sentido contrarreloj.")
    print("Si solo ves 'No se ha detectado sonido.', incrementa la sensibilidad girando el potenciometro en sentido horario.")
    while True:
        detect_sound()  # Check sound sensor status
        time.sleep(0.1) 
        
except KeyboardInterrupt:
    print("Programa termiinado por el usario.")
finally:
    GPIO.cleanup() # Clean up GPIO settings on exit
