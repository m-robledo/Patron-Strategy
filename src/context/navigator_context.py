"""
Módulo del Contexto en el Patrón Strategy (Navegador / Google Maps).

El Contexto (NavigatorContext) mantiene referencias a la estrategia de transporte
(IRouteStrategy) y a la estrategia de optimización (IOptimizationStrategy).
Delegará en ellas la planificación de la ruta sin bloques condicionales (if/else).
"""

from typing import Optional
from src.strategies.base import IRouteStrategy, IOptimizationStrategy, RouteResult


class NavigatorContext:
    """
    Clase Contexto (Context).

    El Navegador interactúa con el cliente recibiendo origen, destino y distancia,
    y delega en las estrategias activas el cálculo y ajuste de la ruta óptima.
    """

    def __init__(
        self,
        route_strategy: Optional[IRouteStrategy] = None,
        optimization_strategy: Optional[IOptimizationStrategy] = None,
    ):
        """
        Inicializa el Navegador con las estrategias recibidas.
        """
        self._route_strategy = route_strategy
        self._optimization_strategy = optimization_strategy

    @property
    def route_strategy(self) -> Optional[IRouteStrategy]:
        """Obtiene la estrategia de transporte actual."""
        return self._route_strategy

    @route_strategy.setter
    def route_strategy(self, strategy: IRouteStrategy) -> None:
        """
        Permite cambiar dinámicamente el medio de transporte en tiempo de ejecución.
        """
        if not isinstance(strategy, IRouteStrategy):
            raise TypeError("La estrategia debe implementar IRouteStrategy.")
        self._route_strategy = strategy

    @property
    def optimization_strategy(self) -> Optional[IOptimizationStrategy]:
        """Obtiene la estrategia de optimización actual."""
        return self._optimization_strategy

    @optimization_strategy.setter
    def optimization_strategy(self, strategy: IOptimizationStrategy) -> None:
        """
        Permite cambiar dinámicamente el criterio de optimización en tiempo de ejecución.
        """
        if not isinstance(strategy, IOptimizationStrategy):
            raise TypeError("La estrategia debe implementar IOptimizationStrategy.")
        self._optimization_strategy = strategy

    def plan_route(self, origin: str, destination: str, distance_km: float) -> RouteResult:
        """
        Delega la planificación a las estrategias configuradas.

        :param origin: Punto de partida.
        :param destination: Punto de llegada.
        :param distance_km: Distancia base en kilómetros.
        :return: RouteResult optimizado.
        """
        if self._route_strategy is None:
            raise RuntimeError("No se ha configurado una estrategia de transporte (IRouteStrategy).")

        # 1. Delegación pura en la estrategia de transporte (Cálculo base)
        base_route = self._route_strategy.calculate_route(origin, destination, distance_km)

        # 2. Delegación en la estrategia de optimización (si fue provista)
        if self._optimization_strategy is not None:
            return self._optimization_strategy.apply_optimization(base_route)

        return base_route
