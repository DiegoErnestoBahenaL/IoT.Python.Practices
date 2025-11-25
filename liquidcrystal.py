import RPi.GPIO as GPIO
import time

# LCD command constants (mismos valores que LiquidCrystal.h de Arduino)
LCD_CLEARDISPLAY   = 0x01
LCD_RETURNHOME     = 0x02
LCD_ENTRYMODESET   = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT    = 0x10
LCD_FUNCTIONSET    = 0x20
LCD_SETCGRAMADDR   = 0x40
LCD_SETDDRAMADDR   = 0x80

# flags para modo de entrada
LCD_ENTRYRIGHT          = 0x00
LCD_ENTRYLEFT           = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags para display on/off
LCD_DISPLAYON  = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON   = 0x02
LCD_CURSOROFF  = 0x00
LCD_BLINKON    = 0x01
LCD_BLINKOFF   = 0x00

# flags para scroll display/cursor
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE  = 0x00
LCD_MOVERIGHT   = 0x04
LCD_MOVELEFT    = 0x00

# flags para Function Set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE    = 0x08
LCD_1LINE    = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS  = 0x00


class LiquidCrystal:
    """
    Port de la librería LiquidCrystal de Arduino para Raspberry Pi usando RPi.GPIO.
    Por defecto usa modo de 4 bits con pines d4-d7.
    Opcionalmente soporta 8 bits si también se pasan d0-d3.
    """

    def __init__(self, rs, enable, d4, d5, d6, d7,
                 rw=None, d0=None, d1=None, d2=None, d3=None):
        # Usamos numeración BCM (igual que en tu SoundSensor.py)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self._rs_pin = rs
        self._rw_pin = rw
        self._enable_pin = enable

        if d0 is not None and d1 is not None and d2 is not None and d3 is not None:
            # Modo 8 bits: se reciben los 8 pines de datos
            self._displayfunction = LCD_8BITMODE | LCD_1LINE | LCD_5x8DOTS
            self._data_pins = [d0, d1, d2, d3, d4, d5, d6, d7]
        else:
            # Modo 4 bits: solo se usan las 4 líneas de datos altas (D4–D7 del LCD)
            self._displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS
            # Igual que en los constructores de 4 bits de Arduino:
            # d4–d7 representan D4–D7 físicos del LCD.
            self._data_pins = [d4, d5, d6, d7]

        self._displaycontrol = 0
        self._displaymode = 0
        self._initialized = False

        self._numlines = 1
        self._row_offsets = [0x00, 0x40, 0x00, 0x40]

    # --- API pública (muy parecida a Arduino) ---

    def begin(self, cols, lines, dotsize=LCD_5x8DOTS):
        """
        Inicializa el LCD con el número de columnas y filas especificado.
        Debe llamarse antes de usar el resto de métodos.
        """
        if lines > 1:
            self._displayfunction |= LCD_2LINE
        self._numlines = lines

        # Mismo esquema que la librería original:
        self.setRowOffsets(0x00, 0x40, 0x00 + cols, 0x40 + cols)

        # Para algunos displays de 1 línea se puede usar fuente de 10 puntos
        if (dotsize != LCD_5x8DOTS) and (lines == 1):
            self._displayfunction |= LCD_5x10DOTS

        GPIO.setup(self._rs_pin, GPIO.OUT)
        if self._rw_pin is not None:
            GPIO.setup(self._rw_pin, GPIO.OUT)
        GPIO.setup(self._enable_pin, GPIO.OUT)

        # Data pins
        for pin in self._data_pins:
            GPIO.setup(pin, GPIO.OUT)

        # Secuencia de inicialización (según datasheet HD44780)
        time.sleep(0.05)  # 50 ms después de encender

        GPIO.output(self._rs_pin, GPIO.LOW)
        GPIO.output(self._enable_pin, GPIO.LOW)
        if self._rw_pin is not None:
            GPIO.output(self._rw_pin, GPIO.LOW)

        # Selección 4/8 bits
        if not (self._displayfunction & LCD_8BITMODE):
            # Modo 4 bits: secuencia especial
            self.write4bits(0x03)
            self._delay_microseconds(4500)

            self.write4bits(0x03)
            self._delay_microseconds(4500)

            self.write4bits(0x03)
            self._delay_microseconds(150)

            # Finalmente, establecer interfaz de 4 bits
            self.write4bits(0x02)
        else:
            # Modo 8 bits
            self.command(LCD_FUNCTIONSET | self._displayfunction)
            self._delay_microseconds(4500)

            self.command(LCD_FUNCTIONSET | self._displayfunction)
            self._delay_microseconds(150)

            self.command(LCD_FUNCTIONSET | self._displayfunction)

        # Configura líneas, fuente, etc.
        self.command(LCD_FUNCTIONSET | self._displayfunction)

        # Display encendido, sin cursor y sin blink (por defecto)
        self._displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.display()

        # Limpia pantalla
        self.clear()

        # Dirección de texto por defecto (izquierda a derecha, sin desplazamiento)
        self._displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        self.command(LCD_ENTRYMODESET | self._displaymode)

        self._initialized = True

    def clear(self):
        """Limpia el display y regresa el cursor a (0, 0)."""
        self.command(LCD_CLEARDISPLAY)
        self._delay_microseconds(2000)  # comando lento

    def home(self):
        """Regresa el cursor a (0, 0)."""
        self.command(LCD_RETURNHOME)
        self._delay_microseconds(2000)  # comando lento

    def setCursor(self, col, row):
        """Mueve el cursor a (col, row)."""
        max_lines = len(self._row_offsets)
        if row >= max_lines:
            row = max_lines - 1
        if row >= self._numlines:
            row = self._numlines - 1

        self.command(LCD_SETDDRAMADDR | (col + self._row_offsets[row]))

    # Control de display on/off
    def noDisplay(self):
        self._displaycontrol &= ~LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)

    def display(self):
        self._displaycontrol |= LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)

    # Cursor on/off
    def noCursor(self):
        self._displaycontrol &= ~LCD_CURSORON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)

    def cursor(self):
        self._displaycontrol |= LCD_CURSORON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)

    # Blink on/off
    def noBlink(self):
        self._displaycontrol &= ~LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)

    def blink(self):
        self._displaycontrol |= LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)

    # Scroll
    def scrollDisplayLeft(self):
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)

    def scrollDisplayRight(self):
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

    # Dirección del texto
    def leftToRight(self):
        self._displaymode |= LCD_ENTRYLEFT
        self.command(LCD_ENTRYMODESET | self._displaymode)

    def rightToLeft(self):
        self._displaymode &= ~LCD_ENTRYLEFT
        self.command(LCD_ENTRYMODESET | self._displaymode)

    # Auto-scroll
    def autoscroll(self):
        self._displaymode |= LCD_ENTRYSHIFTINCREMENT
        self.command(LCD_ENTRYMODESET | self._displaymode)

    def noAutoscroll(self):
        self._displaymode &= ~LCD_ENTRYSHIFTINCREMENT
        self.command(LCD_ENTRYMODESET | self._displaymode)

    def setRowOffsets(self, row0, row1, row2, row3):
        self._row_offsets[0] = row0
        self._row_offsets[1] = row1
        self._row_offsets[2] = row2
        self._row_offsets[3] = row3

    def createChar(self, location, charmap):
        """
        Crea un carácter personalizado (ubicación 0-7) con el mapa de 8 bytes.
        charmap debe ser una lista/tupla de 8 enteros (0–31 típicamente).
        """
        location &= 0x7  # solo 0–7 son válidos
        self.command(LCD_SETCGRAMADDR | (location << 3))
        for i in range(8):
            self.write(charmap[i])

    # --- Helpers de impresión ---

    def write(self, value):
        """
        Escritura de bajo nivel.
        - Si value es int: lo manda como un solo byte.
        - Si es string u otro tipo: se convierte a string y se mandan todos los caracteres.
        """
        if isinstance(value, int):
            self._send(value & 0xFF, GPIO.HIGH)
        else:
            for ch in str(value):
                self._send(ord(ch) & 0xFF, GPIO.HIGH)

    def print(self, text):
        """Método estilo Arduino: lcd.print("Hola");"""
        self.write(text)

    # --- Comunicación de bajo nivel ---

    def command(self, value):
        self._send(value, GPIO.LOW)

    def _send(self, value, mode):
        GPIO.output(self._rs_pin, mode)

        # Si hay pin RW, lo dejamos en bajo para escribir
        if self._rw_pin is not None:
            GPIO.output(self._rw_pin, GPIO.LOW)

        if self._displayfunction & LCD_8BITMODE:
            self.write8bits(value)
        else:
            self.write4bits(value >> 4)
            self.write4bits(value & 0x0F)

    def pulseEnable(self):
        GPIO.output(self._enable_pin, GPIO.LOW)
        self._delay_microseconds(1)
        GPIO.output(self._enable_pin, GPIO.HIGH)
        self._delay_microseconds(1)  # pulso > 450 ns
        GPIO.output(self._enable_pin, GPIO.LOW)
        self._delay_microseconds(100)  # comandos necesitan > 37 µs

    def write4bits(self, value):
        for i, pin in enumerate(self._data_pins[:4]):
            GPIO.output(pin, (value >> i) & 0x01)
        self.pulseEnable()

    def write8bits(self, value):
        for i, pin in enumerate(self._data_pins):
            GPIO.output(pin, (value >> i) & 0x01)
        self.pulseEnable()

    # Helper de timing
    def _delay_microseconds(self, microseconds):
        time.sleep(microseconds / 1_000_000.0)

    # Limpieza opcional (por ejemplo, al terminar el programa)
    def cleanup(self):
        GPIO.cleanup()
