"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
"""

import sys
import threading
import time
import random

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10
NUM_ABEJAS = 5
tarro_miel = 0
simulacion_activa = True

# Exclusión mutua sobre la variable compartida.
mutex = threading.Lock()

# El oso permanece bloqueado hasta que el tarro está lleno.
sem_oso = threading.Semaphore(0)

# Permite producir miel mientras el tarro está disponible.
# Cuando está lleno, las abejas quedan bloqueadas hasta que el oso lo vacía.
sem_tarro_disponible = threading.Semaphore(1)


def abeja(id_abeja):
    global tarro_miel, simulacion_activa

    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2))

        sem_tarro_disponible.acquire()

        if not simulacion_activa:
            sem_tarro_disponible.release()
            break

        with mutex:
            if not simulacion_activa:
                sem_tarro_disponible.release()
                break

            tarro_miel += 1
            print(f"🐝 Abeja {id_abeja}: deposita miel. "
                  f"Tarro = {tarro_miel}/{M}")

            if tarro_miel == M:
                print("🍯 Tarro lleno. La abeja despierta al oso.")
                sem_oso.release()
            else:
                # Otra abeja puede continuar produciendo.
                sem_tarro_disponible.release()


def oso(max_tarros=2):
    global tarro_miel, simulacion_activa

    tarros_comidos = 0

    while tarros_comidos < max_tarros:
        # El oso duerme/bloquea hasta que el tarro esté lleno.
        sem_oso.acquire()

        with mutex:
            if tarro_miel == M:
                print(f"🐻 Oso: comienza a comer el tarro con "
                      f"{tarro_miel} porciones de miel.")
                tarro_miel = 0
                tarros_comidos += 1
                print(f"🐻 Oso: terminó de comer. "
                      f"Tarros comidos = {tarros_comidos}/{max_tarros}")

        # El tarro vuelve a estar disponible para las abejas.
        sem_tarro_disponible.release()

        time.sleep(0.05)

    simulacion_activa = False

    # Desbloquear a las abejas que pudieran quedar esperando,
    # para que puedan comprobar que la simulación terminó.
    for _ in range(NUM_ABEJAS):
        sem_tarro_disponible.release()


if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)

    h_oso = threading.Thread(target=oso, args=(2,), name="Oso")

    h_abejas = []
    for i in range(NUM_ABEJAS):
        t = threading.Thread(target=abeja, args=(i,), name=f"Abeja-{i}")
        h_abejas.append(t)

    h_oso.start()

    for t in h_abejas:
        t.start()

    h_oso.join()

    for t in h_abejas:
        t.join()

    print("=" * 60)
    print(" Simulación finalizada correctamente.")
    print(f" Miel restante en el tarro: {tarro_miel}")
    print("=" * 60)
