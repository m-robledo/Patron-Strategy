"""
Paquete de Estrategias para el Planificador de Rutas (Google Maps).
"""

from src.strategies.base import IRouteStrategy, IOptimizationStrategy, RouteResult
from src.strategies.route_strategies import (
    CarRouteStrategy,
    PublicTransitRouteStrategy,
    BicycleRouteStrategy,
    WalkingRouteStrategy,
)
from src.strategies.optimization_strategies import (
    FastestTimeStrategy,
    ShortestDistanceStrategy,
    EconomicStrategy,
)

__all__ = [
    "IRouteStrategy",
    "IOptimizationStrategy",
    "RouteResult",
    "CarRouteStrategy",
    "PublicTransitRouteStrategy",
    "BicycleRouteStrategy",
    "WalkingRouteStrategy",
    "FastestTimeStrategy",
    "ShortestDistanceStrategy",
    "EconomicStrategy",
]
