#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

class Stepper28BYJ48:
    """
    Control para motor 28BYJ-48 + ULN2003 en Raspberry Pi.

    pins: lista [IN1, IN2, IN3, IN4] en numeración BCM.
    mode: 'half' (medio paso, por defecto) o 'full' (paso completo).
    steps_per_rev: pasos por vuelta usados en el cálculo de RPM/ángulos.
                   Aproximado: 4096 en medio paso, 2048 en paso completo.
    """

    HALF_STEP_SEQ = [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1],
    ]

    FULL_STEP_SEQ = [
        [1,0,0,1],
        [1,1,0,0],
        [0,1,1,0],
        [0,0,1,1],
    ]

    def __init__(self, pins, mode='half', steps_per_rev=None):
        if mode not in ('half', 'full'):
            raise ValueError("mode debe ser 'half' o 'full'")
        self.pins = list(pins)
        self.mode = mode
        self.seq = self.HALF_STEP_SEQ if mode == 'half' else self.FULL_STEP_SEQ
        # Valor por defecto típico:
        if steps_per_rev is None:
            self.steps_per_rev = 4096 if mode == 'half' else 2048
        else:
            self.steps_per_rev = int(steps_per_rev)

        # Velocidad por defecto
        self.rpm = 10
        self._calc_delay()

        GPIO.setmode(GPIO.BCM)
        for p in self.pins:
            GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)

        # Índice actual en la secuencia
        self._seq_index = 0

    def _calc_delay(self):
        # tiempo por paso (segundos) = 60 / (rpm * pasos_por_vuelta)
        # Nota: En medio paso hay el doble de micro-pasos que en paso completo.
        self.step_delay = 60.0 / (self.rpm * float(self.steps_per_rev))

    def set_speed(self, rpm):
        """Define RPM del motor."""
        if rpm <= 0:
            raise ValueError("rpm debe ser > 0")
        self.rpm = float(rpm)
        self._calc_delay()

    def _write_coils(self, pattern):
        for pin, val in zip(self.pins, pattern):
            GPIO.output(pin, GPIO.HIGH if val else GPIO.LOW)

    def _step_once(self, direction=1):
        """Avanza un micro-paso en la secuencia."""
        self._seq_index = (self._seq_index + direction) % len(self.seq)
        self._write_coils(self.seq[self._seq_index])
        time.sleep(self.step_delay)

    def step(self, steps, direction=1, release=True):
        """
        Mueve 'steps' micro-pasos (elementos de la secuencia).
        direction: 1 = horario, -1 = antihorario.
        release: si True, desactiva bobinas al final (menos calentamiento).
        """
        direction = 1 if direction >= 0 else -1
        for _ in range(int(steps)):
            self._step_once(direction)
        if release:
            self.release()

    def rotate(self, turns, direction=1, release=True):
        """Gira 'turns' vueltas completas."""
        steps = int(abs(turns) * self.steps_per_rev)
        self.step(steps, direction=direction if turns >= 0 else -direction, release=release)

    def angle(self, degrees, direction=1, release=True):
        """Gira 'degrees' grados."""
        steps = int(abs(degrees) / 360.0 * self.steps_per_rev)
        self.step(steps, direction=direction if degrees >= 0 else -direction, release=release)

    def release(self):
        """Desenergiza las bobinas (baja consumo/calor)."""
        for p in self.pins:
            GPIO.output(p, GPIO.LOW)

    def cleanup(self):
        """Libera los GPIO (llamar al finalizar)."""
        self.release()
        GPIO.cleanup()

def main():
    # Define tus GPIO (BCM) conectados a IN1..IN4 del ULN2003
    PINS = [17, 18, 27, 22]  # IN1, IN2, IN3, IN4
    # Modo: 'half' para mayor resolución (≈4096 pasos/vuelta), 'full' para más torque
    motor = Stepper28BYJ48(PINS, mode='half')  # steps_per_rev por defecto

    try:
        print("Ejemplo: 2 vueltas horario @12 RPM")
        motor.set_speed(12)
        motor.rotate(2, direction=1)

        print("Ejemplo: 2 vueltas anti-horario @12 RPM")
        motor.set_speed(12)
        motor.rotate(2, direction=-1)


        print("Listo.")
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
    finally:
        motor.cleanup()

if __name__ == "__main__":
    main()
