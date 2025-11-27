import RPi.GPIO as GPIO
import time

# Pines BCM de la Raspberry Pi 5 (recomendados de uso general)
S3_PIN  = 24   # S3 del TCS230  (pin físico 18)
S2_PIN  = 23   # S2 del TCS230  (pin físico 16)
OUT_PIN = 25   # OUT del TCS230 (pin físico 22)

# Configuración inicial de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(S2_PIN, GPIO.OUT)
GPIO.setup(S3_PIN, GPIO.OUT)
GPIO.setup(OUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def set_filter(color: str) -> None:
    """
    Selecciona el filtro de color del TCS230 mediante S2 y S3.

    Tabla típica TCS230/TCS3200:
      S2 S3
      0  0  -> Rojo
      0  1  -> Azul
      1  0  -> Claro (sin filtro)
      1  1  -> Verde
    """
    color = color.lower()
    if color == "red" or color == "rojo":
        GPIO.output(S2_PIN, GPIO.LOW)
        GPIO.output(S3_PIN, GPIO.LOW)
    elif color == "blue" or color == "azul":
        GPIO.output(S2_PIN, GPIO.LOW)
        GPIO.output(S3_PIN, GPIO.HIGH)
    elif color == "clear" or color == "claro":
        GPIO.output(S2_PIN, GPIO.HIGH)
        GPIO.output(S3_PIN, GPIO.LOW)
    elif color == "green" or color == "verde":
        GPIO.output(S2_PIN, GPIO.HIGH)
        GPIO.output(S3_PIN, GPIO.HIGH)
    else:
        raise ValueError(f"Color de filtro no válido: {color}")

def measure_frequency(sample_time: float = 0.1) -> float:
    """
    Mide la frecuencia en Hz contando los flancos de subida en OUT
    durante 'sample_time' segundos.
    """
    count = 0
    start = time.time()
    last_state = GPIO.input(OUT_PIN)

    while (time.time() - start) < sample_time:
        state = GPIO.input(OUT_PIN)
        # Detectar flanco de subida
        if last_state == GPIO.LOW and state == GPIO.HIGH:
            count += 1
        last_state = state

    # frecuencia = pulsos / tiempo_muestreo
    freq = count / sample_time
    return freq

def read_raw_rgb(sample_time: float = 0.1):
    """
    Lee las frecuencias crudas para R, G y B.
    Devuelve un diccionario con las frecuencias en Hz.
    """
    readings = {}

    # Rojo
    set_filter("red")
    time.sleep(0.02)  # pequeño tiempo para estabilizar
    readings["red"] = measure_frequency(sample_time)

    # Verde
    set_filter("green")
    time.sleep(0.02)
    readings["green"] = measure_frequency(sample_time)

    # Azul
    set_filter("blue")
    time.sleep(0.02)
    readings["blue"] = measure_frequency(sample_time)

    return readings

def normalize_rgb(freq_rgb, min_freq=200.0, max_freq=20000.0):
    """
    Normaliza las frecuencias a un rango 0–255 (aprox).
    Ajusta min_freq y max_freq según tu calibración.
    El TCS230 entrega más frecuencia cuanto más intensa es la luz.
    """
    rgb_norm = {}
    for color, f in freq_rgb.items():
        # Limitar a rango esperado
        f_clamped = max(min(f, max_freq), min_freq)
        # Escalar linealmente a 0–255
        value = int(255 * (f_clamped - min_freq) / (max_freq - min_freq))
        rgb_norm[color] = value
    return rgb_norm

if __name__ == "__main__":
    try:
        while True:
            freqs = read_raw_rgb(sample_time=0.1)
            rgb = normalize_rgb(freqs)

            print("Frecuencias (Hz): "
                  f"R={freqs['red']:.1f}, G={freqs['green']:.1f}, B={freqs['blue']:.1f}")
            print("RGB aproximado (0–255): "
                  f"R={rgb['red']}, G={rgb['green']}, B={rgb['blue']}")
            print("-" * 50)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nSaliendo...")

    finally:
        GPIO.cleanup()
