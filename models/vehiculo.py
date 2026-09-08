from abc import ABC, abstractmethod


class Vehiculo(ABC):
    """Clase base para los vehículos que participan en la simulación."""

    def __init__(self, codigo: str, nombre: str, piloto: str):
        self.__codigo = self._validar_texto(codigo, "código", 2, 20)
        self.__nombre = self._validar_texto(nombre, "nombre", 2, 50)
        self.__piloto = self._validar_texto(piloto, "piloto", 2, 50)
        self.__distancia = 0.0

    @staticmethod
    def _validar_texto(valor: str, campo: str, minimo: int, maximo: int) -> str:
        if not isinstance(valor, str):
            raise TypeError(f"El {campo} debe ser texto.")
        limpio = " ".join(valor.strip().split())
        if not minimo <= len(limpio) <= maximo:
            raise ValueError(f"El {campo} debe tener entre {minimo} y {maximo} caracteres.")
        return limpio

    @property
    def codigo(self) -> str:
        return self.__codigo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def piloto(self) -> str:
        return self.__piloto

    @piloto.setter
    def piloto(self, valor: str) -> None:
        self.__piloto = self._validar_texto(valor, "piloto", 2, 50)

    @property
    def distancia(self) -> float:
        return round(self.__distancia, 2)

    def reiniciar(self) -> None:
        self.__distancia = 0.0

    def registrar_avance(self, metros: float) -> float:
        if isinstance(metros, bool) or not isinstance(metros, (int, float)):
            raise TypeError("El avance debe ser numérico.")
        if metros <= 0:
            raise ValueError("El avance debe ser mayor que cero.")
        self.__distancia += float(metros)
        return self.distancia

    @property
    @abstractmethod
    def tipo(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def calcular_avance(self, avance_base: float, variacion: float) -> float:
        """Calcula el avance del tramo. Cada subclase implementa su propia regla."""
        raise NotImplementedError

    def resumen(self) -> dict:
        return {
            "Código": self.codigo,
            "Tipo": self.tipo,
            "Vehículo": self.nombre,
            "Piloto": self.piloto,
            "Distancia": self.distancia,
        }


class Deportivo(Vehiculo):
    @property
    def tipo(self) -> str:
        return "Deportivo"

    def calcular_avance(self, avance_base: float, variacion: float) -> float:
        return max(1.0, float(avance_base) * 1.18 * float(variacion))


class Clasico(Vehiculo):
    @property
    def tipo(self) -> str:
        return "Clásico"

    def calcular_avance(self, avance_base: float, variacion: float) -> float:
        return max(1.0, float(avance_base) * 0.96 * float(variacion))


class UsoDiario(Vehiculo):
    @property
    def tipo(self) -> str:
        return "Uso diario"

    def calcular_avance(self, avance_base: float, variacion: float) -> float:
        return max(1.0, float(avance_base) * 1.00 * float(variacion))


class VehiculoFactory:
    """Centraliza la creación de subclases para mantener simple la interfaz."""

    TIPOS = ("Deportivo", "Clásico", "Uso diario")

    @staticmethod
    def crear(tipo: str, codigo: str, nombre: str, piloto: str) -> Vehiculo:
        clases = {
            "Deportivo": Deportivo,
            "Clásico": Clasico,
            "Uso diario": UsoDiario,
        }
        clase = clases.get(tipo)
        if not clase:
            raise ValueError("Tipo de vehículo no válido.")
        return clase(codigo, nombre, piloto)
