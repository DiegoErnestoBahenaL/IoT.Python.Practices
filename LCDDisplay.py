from RPi import GPIO          # Esto en Pi 5 en realidad viene de rpi-lgpio
from RPLCD.gpio import CharLCD
import time

# Configurar el LCD en modo 4 bits
lcd = CharLCD(
    pin_rs=19,               # GPIO RS
    pin_e=26,                # GPIO E
    pin_rw=None,             # RW a GND en hardware
    pins_data=[13, 6, 5, 11],# D4, D5, D6, D7
    numbering_mode=GPIO.BCM, # Usamos numeración BCM
    cols=16,
    rows=2
)

try:
    lcd.write_string('Hola, mundo!')
    lcd.cursor_pos = (1, 0)  # Fila 2, columna 0
    lcd.write_string('Raspberry Pi 5')
    time.sleep(5)
finally:
    lcd.clear()
    lcd.close()
    GPIO.cleanup()
