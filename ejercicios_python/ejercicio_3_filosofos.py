"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026

Ejercicio Práctico N° 3: La Cena de los Filósofos (Prevención de Deadlock)
"""

import threading
import time
import random

NUM_FILOSOFOS = 5

# Cada tenedor está representado por un Lock.
tenedores = [threading.Lock() for _ in range(NUM_FILOSOFOS)]

# Cantidad de veces que comió cada filósofo.
comidas = [0] * NUM_FILOSOFOS

lock_print = threading.Lock()


def log(msg):
    with lock_print:
        print(msg)


def pensar(id):
    log(f"🤔 Filósofo {id} está pensando...")
    time.sleep(random.uniform(0.1, 0.3))


def comer(id):
    log(f"🍝 Filósofo {id} está comiendo espagueti...")
    comidas[id] += 1
    time.sleep(random.uniform(0.1, 0.3))
    log(f"✨ Filósofo {id} terminó de comer "
        f"(total comidas: {comidas[id]}).")


def filosofo(id, rondas=3):
    """
    Solución asimétrica para evitar Deadlock.

    Filósores pares: toman primero el tenedor izquierdo.
    Filósofos impares: toman primero el tenedor derecho.

    Al romper la espera circular se evita el interbloqueo.
    """

    for _ in range(rondas):
        pensar(id)

        tenedor_izq = id
        tenedor_der = (id + 1) % NUM_FILOSOFOS

        # Estrategia asimétrica:
        # pares -> izquierdo primero
        # impares -> derecho primero
        if id % 2 == 0:
            primero = tenedor_izq
            segundo = tenedor_der
        else:
            primero = tenedor_der
            segundo = tenedor_izq

        tenedores[primero].acquire()

        try:
            tenedores[segundo].acquire()

            try:
                comer(id)
            finally:
                tenedores[segundo].release()

        finally:
            tenedores[primero].release()


if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación de los Filósofos Comensales (UNJu FI)")
    print("=" * 60)

    hilos = []

    for i in range(NUM_FILOSOFOS):
        t = threading.Thread(
            target=filosofo,
            args=(i, 3),
            name=f"Filosofo-{i}"
        )
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    print("=" * 60)
    print(" Resumen de Comidas:")
    for i, c in enumerate(comidas):
        print(f" - Filósofo {i}: {c} veces comió.")

    print(" ¡Simulación completada sin Interbloqueo (Deadlock)!")
    print("=" * 60)
