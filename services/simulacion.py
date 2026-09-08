from dataclasses import dataclass
from time import perf_counter, sleep
import random
import threading


@dataclass(frozen=True)
class PasoPlan:
    espera: float
    variacion: float


class SimuladorCarrera:
    """Ejecuta la misma carga de trabajo de forma secuencial y concurrente."""

    def __init__(self, tramos=6, avance_base=100.0, espera_min=0.12, espera_max=0.30):
        if not 2 <= int(tramos) <= 20:
            raise ValueError("La cantidad de tramos debe estar entre 2 y 20.")
        if float(avance_base) <= 0:
            raise ValueError("El avance base debe ser mayor que cero.")
        if float(espera_min) <= 0 or float(espera_max) < float(espera_min):
            raise ValueError("El intervalo de espera configurado no es válido.")
        self._tramos = int(tramos)
        self._avance_base = float(avance_base)
        self._espera_min = float(espera_min)
        self._espera_max = float(espera_max)
        self._lock = threading.Lock()

    def crear_plan(self, vehiculos, semilla=30):
        """Precalcula esperas y variaciones para comparar ambos modos con la misma carga."""
        rng = random.Random(int(semilla))
        plan = {}
        for vehiculo in vehiculos:
            plan[vehiculo.codigo] = [
                PasoPlan(
                    espera=rng.uniform(self._espera_min, self._espera_max),
                    variacion=rng.uniform(0.88, 1.12),
                )
                for _ in range(self._tramos)
            ]
        return plan

    def _procesar_vehiculo(self, vehiculo, pasos, historia, resultados, modo):
        vehiculo.reiniciar()
        inicio = perf_counter()
        for numero, paso in enumerate(pasos, start=1):
            sleep(paso.espera)
            avance = vehiculo.calcular_avance(self._avance_base, paso.variacion)
            acumulado = vehiculo.registrar_avance(avance)
            fila = {
                "Modo": modo,
                "Código": vehiculo.codigo,
                "Tipo": vehiculo.tipo,
                "Vehículo": vehiculo.nombre,
                "Piloto": vehiculo.piloto,
                "Tramo": numero,
                "Espera_s": round(paso.espera, 3),
                "Avance": round(avance, 2),
                "Distancia": acumulado,
            }
            with self._lock:
                historia.append(fila)
        duracion = perf_counter() - inicio
        with self._lock:
            resultados.append(
                {
                    "Código": vehiculo.codigo,
                    "Tipo": vehiculo.tipo,
                    "Vehículo": vehiculo.nombre,
                    "Piloto": vehiculo.piloto,
                    "Distancia": vehiculo.distancia,
                    "Tiempo_individual_s": round(duracion, 3),
                }
            )

    def ejecutar_secuencial(self, vehiculos, plan):
        historia = []
        resultados = []
        inicio = perf_counter()
        for vehiculo in vehiculos:
            self._procesar_vehiculo(
                vehiculo,
                plan[vehiculo.codigo],
                historia,
                resultados,
                "Secuencial",
            )
        total = perf_counter() - inicio
        return sorted(resultados, key=lambda x: x["Distancia"], reverse=True), historia, total

    def ejecutar_concurrente(self, vehiculos, plan):
        historia = []
        resultados = []
        hilos = []
        inicio = perf_counter()
        for vehiculo in vehiculos:
            hilo = threading.Thread(
                target=self._procesar_vehiculo,
                args=(
                    vehiculo,
                    plan[vehiculo.codigo],
                    historia,
                    resultados,
                    "Concurrente",
                ),
                name=f"Vehiculo-{vehiculo.codigo}",
            )
            hilos.append(hilo)
            hilo.start()
        for hilo in hilos:
            hilo.join()
        total = perf_counter() - inicio
        return sorted(resultados, key=lambda x: x["Distancia"], reverse=True), historia, total

    @staticmethod
    def comparar(tiempo_secuencial, tiempo_concurrente):
        sec = float(tiempo_secuencial)
        con = float(tiempo_concurrente)
        if sec <= 0 or con <= 0:
            raise ValueError("Los tiempos deben ser mayores que cero.")
        ahorro = max(0.0, sec - con)
        return {
            "Secuencial_s": round(sec, 3),
            "Concurrente_s": round(con, 3),
            "Ahorro_s": round(ahorro, 3),
            "Reducción_%": round((ahorro / sec) * 100, 2),
            "Aceleración_x": round(sec / con, 2),
        }
