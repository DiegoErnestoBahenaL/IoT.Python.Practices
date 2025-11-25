from liquidcrystal import LiquidCrystal
from time import sleep

# Ajusta los números según tu cableado (BCM)
lcd = LiquidCrystal(
    rs=26,
    enable=19,
    d4=13,
    d5=6,
    d6=5,
    d7=11,
    rw=None  # o simplemente omitirlo si RW está a GND
)

try:
    lcd.begin(16, 2)     # 16x2
    lcd.clear()
    lcd.print("Hola, Diegoooooooooo000!")
    lcd.setCursor(0, 1)  # columna 0, fila 1
    lcd.print("Port OK :)")

    while True:
        # Solo mantener el texto en pantalla
        sleep(1)

except KeyboardInterrupt:
    pass
finally:
    lcd.cleanup()
