"""
Módulo de Interfaces Base para el Patrón Strategy (Navegación / Google Maps).

Define los contratos abstractos (Interfaces) que todas las estrategias
concretas de ruta y optimización deben implementar.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class RouteResult:
    """
    Estructura de datos que contiene el resultado del cálculo de una ruta.
    """
    transport_name: str
    distance_km: float
    duration_minutes: float
    monetary_cost_ars: float
    calories_burned: float
    co2_saved_kg: float
    estimated_steps: int
    waypoints: List[str]
    notes: str


class IRouteStrategy(ABC):
    """
    Interfaz / Abstracción principal para las Estrategias de Transporte (Medio de Locomoción).

    En el patrón Strategy, esta interfaz declara la operación común para
    todos los algoritmos de navegación soportados (Auto, Colectivo, Bici, A Pie).
    """

    @property
    @abstractmethod
    def transport_type(self) -> str:
        """Nombre descriptivo del medio de transporte."""
        pass

    @property
    @abstractmethod
    def icon(self) -> str:
        """Icono representativo (Emoji o SVG)."""
        pass

    @abstractmethod
    def calculate_route(self, origin: str, destination: str, distance_km: float) -> RouteResult:
        """
        Calcula la ruta en base a los parámetros del trayecto.

        :param origin: Punto de partida (ej: "Centro").
        :param destination: Punto de llegada (ej: "Universidad").
        :param distance_km: Distancia base en kilómetros.
        :return: Instancia de RouteResult con tiempos, costos e itinerario.
        """
        pass


class IOptimizationStrategy(ABC):
    """
    Interfaz / Abstracción secundaria para las Estrategias de Optimización (Criterio de Navegación).

    Declara el método común para ajustar la duración o costo según el criterio
    elegido por el usuario (Más Rápida, Más Corta, Económica).
    """

    @property
    @abstractmethod
    def criterion_name(self) -> str:
        """Nombre del criterio de optimización."""
        pass

    @abstractmethod
    def apply_optimization(self, base_result: RouteResult) -> RouteResult:
        """
        Ajusta la ruta calculada según el criterio de optimización.

        :param base_result: Resultado base calculado por la estrategia de transporte.
        :return: RouteResult optimizado.
        """
        pass
