from gpiozero import DistanceSensor
from time import sleep

ultrasonic = DistanceSensor(echo=17, trigger=4)

try:

    while True:

        print( f" Objeto detectado a {ultrasonic.distance * 100:.2f} cm.")
        sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user.")
