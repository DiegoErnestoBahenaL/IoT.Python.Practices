import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

# Set the GPIO mode (BCM is recommended)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the GPIO pin connected to the DHT11 data line
# Replace 'board.D17' with the actual GPIO pin you are using (e.g., board.D4, board.D23)
dhtDevice = adafruit_dht.DHT11(board.D17)

print("Reading DHT11 sensor data...")

while True:
    try:
        # Read temperature and humidity
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

        # Convert temperature to Fahrenheit
        temperature_f = temperature_c * (9 / 5) + 32

        # Print the readings
        print(
            "Temp: {:.1f} F / {:.1f} C | Humidity: {}%".format(
                temperature_f, temperature_c, humidity
            )
        )

    except RuntimeError as error:
        # Errors can occur, especially with DHT sensors. Just print and continue.
        print(f"Error reading DHT11: {error.args[0]}")

    except Exception as error:
        # Handle other unexpected errors
        dhtDevice.exit()
        raise error

    # Wait for 2 seconds before taking the next reading
    time.sleep(2.0)