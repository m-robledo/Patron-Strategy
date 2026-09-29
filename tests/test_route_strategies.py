"""
Pruebas Unitarias para el Navegador de Rutas / Google Maps (Patrón Strategy).

Cubre:
1. Estrategias de Transporte (CarRouteStrategy, PublicTransitRouteStrategy, BicycleRouteStrategy, WalkingRouteStrategy).
2. Estrategias de Optimización (FastestTimeStrategy, ShortestDistanceStrategy, EconomicStrategy).
3. Contexto (NavigatorContext) y cambio dinámico en runtime.
"""

import unittest
import sys
import os

# Permitir importaciones de src desde tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.strategies import (
    CarRouteStrategy,
    PublicTransitRouteStrategy,
    BicycleRouteStrategy,
    WalkingRouteStrategy,
    FastestTimeStrategy,
    ShortestDistanceStrategy,
    EconomicStrategy,
)
from src.context import NavigatorContext


class TestRouteStrategies(unittest.TestCase):
    """Pruebas unitarias para las estrategias de transporte."""

    def test_car_route_strategy(self):
        strategy = CarRouteStrategy()
        # 60 km -> 60 min, combustible 60*180 = 10800, peaje = 800 (dist > 10)
        res = strategy.calculate_route("Origen", "Destino", 60.0)
        self.assertEqual(res.duration_minutes, 60.0)
        self.assertEqual(res.monetary_cost_ars, 11600.0)
        self.assertEqual(res.co2_saved_kg, 0.0)

    def test_public_transit_strategy(self):
        strategy = PublicTransitRouteStrategy()
        # 10 km -> travel (10/25)*60 = 24 min + 8 waiting = 32 min
        # fare = 450 + 10*30 = 750 ARS
        res = strategy.calculate_route("Origen", "Destino", 10.0)
        self.assertEqual(res.duration_minutes, 32.0)
        self.assertEqual(res.monetary_cost_ars, 750.0)
        self.assertGreater(res.co2_saved_kg, 0.0)

    def test_bicycle_strategy(self):
        strategy = BicycleRouteStrategy()
        # 15 km -> 60 min, 0 ARS, 450 kcal
        res = strategy.calculate_route("Origen", "Destino", 15.0)
        self.assertEqual(res.duration_minutes, 60.0)
        self.assertEqual(res.monetary_cost_ars, 0.0)
        self.assertEqual(res.calories_burned, 450.0)

    def test_walking_strategy(self):
        strategy = WalkingRouteStrategy()
        # 5 km -> 60 min, 0 ARS, 5*1350 = 6750 steps
        res = strategy.calculate_route("Origen", "Destino", 5.0)
        self.assertEqual(res.duration_minutes, 60.0)
        self.assertEqual(res.monetary_cost_ars, 0.0)
        self.assertEqual(res.estimated_steps, 6750)

    def test_invalid_distance_raises_error(self):
        strategy = CarRouteStrategy()
        with self.assertRaises(ValueError):
            strategy.calculate_route("Origen", "Destino", 0.0)


class TestOptimizationStrategies(unittest.TestCase):
    """Pruebas unitarias para las estrategias de optimización."""

    def test_fastest_time_optimization(self):
        car = CarRouteStrategy()
        opt = FastestTimeStrategy()
        base = car.calculate_route("Origen", "Destino", 60.0)  # 60 min base
        optimized = opt.apply_optimization(base)
        self.assertEqual(optimized.duration_minutes, 54.0)  # 60 * 0.90

    def test_shortest_distance_optimization(self):
        car = CarRouteStrategy()
        opt = ShortestDistanceStrategy()
        base = car.calculate_route("Origen", "Destino", 10.0)
        optimized = opt.apply_optimization(base)
        self.assertEqual(optimized.distance_km, 9.5)  # 10 * 0.95


class TestNavigatorContext(unittest.TestCase):
    """Pruebas unitarias para el Contexto (NavigatorContext) y cambio dinámico."""

    def test_navigator_dynamic_strategy_switching(self):
        navigator = NavigatorContext()

        # Inyectamos Auto + Más Rápida
        navigator.route_strategy = CarRouteStrategy()
        navigator.optimization_strategy = FastestTimeStrategy()

        res1 = navigator.plan_route("Obelisco", "Palermo", 6.0)
        self.assertEqual(res1.transport_name, "Automóvil (Vías Rápidas / Autopista)")

        # Cambiamos dinámicamente en runtime a Bicicleta + Económica
        navigator.route_strategy = BicycleRouteStrategy()
        navigator.optimization_strategy = EconomicStrategy()

        res2 = navigator.plan_route("Obelisco", "Palermo", 6.0)
        self.assertEqual(res2.transport_name, "Bicicleta (Red de Ciclovías / Bicisendas)")
        self.assertEqual(res2.monetary_cost_ars, 0.0)

    def test_navigator_raises_error_without_route_strategy(self):
        navigator = NavigatorContext()
        with self.assertRaises(RuntimeError):
            navigator.plan_route("Origen", "Destino", 10.0)


if __name__ == "__main__":
    unittest.main()
