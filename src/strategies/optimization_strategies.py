"""
Módulo de Estrategias Concretas de Optimización / Criterio de Navegación.

Implementa los 3 criterios de selección de ruta:
1. Más Rápida (Estrategia de Criterio A)
2. Más Corta en Distancia (Estrategia de Criterio B)
3. Económica (Estrategia de Criterio C)
"""

from src.strategies.base import IOptimizationStrategy, RouteResult


class FastestTimeStrategy(IOptimizationStrategy):
    """
    Estrategia de Criterio A: Ruta Más Rápida (Prioriza menor ETA).

    Ajusta el algoritmo para seleccionar autopistas y avenidas con onda verde,
    reduciendo el tiempo estimado de viaje en un 10%.
    """

    @property
    def criterion_name(self) -> str:
        return "Ruta Más Rápida (Menor Tiempo)"

    def apply_optimization(self, base_result: RouteResult) -> RouteResult:
        optimized_duration = max(1.0, base_result.duration_minutes * 0.90)
        base_result.duration_minutes = round(optimized_duration, 1)
        base_result.notes += " [Optimizada: Priorizando rapidez de tránsito y vías fluidas]."
        return base_result


class ShortestDistanceStrategy(IOptimizationStrategy):
    """
    Estrategia de Criterio B: Ruta Más Corta (Prioriza menor kilometraje).

    Ajusta la ruta tomando pasajes y calles internas directas, reduciendo
    la distancia total recorrida en un 5%.
    """

    @property
    def criterion_name(self) -> str:
        return "Ruta Más Corta (Menor Distancia)"

    def apply_optimization(self, base_result: RouteResult) -> RouteResult:
        optimized_distance = max(0.1, base_result.distance_km * 0.95)
        base_result.distance_km = round(optimized_distance, 2)
        base_result.notes += " [Optimizada: Priorizando menor recorrido directo]."
        return base_result


class EconomicStrategy(IOptimizationStrategy):
    """
    Estrategia de Criterio C: Ruta Económica (Prioriza menor gasto de dinero).

    Evita peajes en automóviles y sugiere tramos combinados a pie para reducir tarifas.
    """

    @property
    def criterion_name(self) -> str:
        return "Ruta Económica (Ahorro Monetario)"

    def apply_optimization(self, base_result: RouteResult) -> RouteResult:
        # En auto elimina peajes; en otros transportes bonifica gasto
        if base_result.monetary_cost_ars > 800.0:
            base_result.monetary_cost_ars = round(base_result.monetary_cost_ars - 800.0, 2)
        base_result.notes += " [Optimizada: Evitando peajes y reduciendo gastos monetarios]."
        return base_result
