"""
Pruebas Unitarias para la Calculadora de Envíos y Descuentos (Patrón Strategy).

Cubre:
1. Estrategias de Envío (Correo Argentino, Andreani, PedidosYa).
2. Estrategias de Descuento (Regular, Mayorista, VIP).
3. Contexto (OrderCalculator) y cambio dinámico de estrategia en runtime.
"""

import unittest
import sys
import os

# Permitir importaciones de src desde tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.strategies import (
    CorreoArgentinoShipping,
    AndreaniShipping,
    PedidosYaShipping,
    RegularUserDiscount,
    WholesaleDiscount,
    VipUserDiscount,
)
from src.context import OrderCalculator


class TestShippingStrategies(unittest.TestCase):
    """Pruebas unitarias para las estrategias de envío."""

    def test_correo_argentino_standard(self):
        strategy = CorreoArgentinoShipping()
        # Base (1200) + 2kg * 350 (700) + 10km * 8 (80) = 1980.0
        cost = strategy.calculate(weight_kg=2.0, distance_km=10.0, order_value=20000.0)
        self.assertEqual(cost, 1980.0)

    def test_correo_argentino_with_bonus(self):
        strategy = CorreoArgentinoShipping()
        # Order value >= 50000 -> 50% bonificación en envío
        # Costo base sin bono: 1200 + 700 + 80 = 1980.0 -> con 50% desc = 990.0
        cost = strategy.calculate(weight_kg=2.0, distance_km=10.0, order_value=60000.0)
        self.assertEqual(cost, 990.0)

    def test_correo_argentino_invalid_inputs(self):
        strategy = CorreoArgentinoShipping()
        with self.assertRaises(ValueError):
            strategy.calculate(weight_kg=-1.0, distance_km=10.0, order_value=1000.0)

    def test_andreani_weight_tiers(self):
        strategy = AndreaniShipping()
        
        # Tier 1: <= 5kg (+500) -> Base 2500 + 500 + 10km*12 (120) = 3120.0
        cost1 = strategy.calculate(weight_kg=3.0, distance_km=10.0, order_value=10000.0)
        self.assertEqual(cost1, 3120.0)

        # Tier 2: 5-15kg (+1200) -> Base 2500 + 1200 + 120 = 3820.0
        cost2 = strategy.calculate(weight_kg=10.0, distance_km=10.0, order_value=10000.0)
        self.assertEqual(cost2, 3820.0)

        # Tier 3: > 15kg (+2500) -> Base 2500 + 2500 + 120 = 5120.0
        cost3 = strategy.calculate(weight_kg=20.0, distance_km=10.0, order_value=10000.0)
        self.assertEqual(cost3, 5120.0)

    def test_pedidos_ya_urban_success(self):
        strategy = PedidosYaShipping()
        # Base 800 + 5km*150 (750) = 1550.0 (peso <= 5kg)
        cost = strategy.calculate(weight_kg=2.0, distance_km=5.0, order_value=5000.0)
        self.assertEqual(cost, 1550.0)

    def test_pedidos_ya_heavy_surcharge(self):
        strategy = PedidosYaShipping()
        # Base 800 + 5km*150 (750) + Recargo peso > 5kg (600) = 2150.0
        cost = strategy.calculate(weight_kg=8.0, distance_km=5.0, order_value=5000.0)
        self.assertEqual(cost, 2150.0)

    def test_pedidos_ya_out_of_range_raises_error(self):
        strategy = PedidosYaShipping()
        # Distancia 20 km > 15 km max -> debe lanzar ValueError
        with self.assertRaises(ValueError):
            strategy.calculate(weight_kg=2.0, distance_km=20.0, order_value=5000.0)


class TestDiscountStrategies(unittest.TestCase):
    """Pruebas unitarias para las estrategias de descuento."""

    def test_regular_user_discount(self):
        strategy = RegularUserDiscount()
        # Compra < $100.000 -> $0 descuento
        self.assertEqual(strategy.calculate_discount(50000.0), 0.0)
        # Compra >= $100.000 -> 3% de descuento ($3.000)
        self.assertEqual(strategy.calculate_discount(100000.0), 3000.0)

    def test_wholesale_user_discount(self):
        strategy = WholesaleDiscount()
        # Compra < $80.000 -> 15% ($1.500 sobre $10.000)
        self.assertEqual(strategy.calculate_discount(10000.0), 1500.0)
        # Compra >= $80.000 -> 20% ($20.000 sobre $100.000)
        self.assertEqual(strategy.calculate_discount(100000.0), 20000.0)

    def test_vip_user_discount(self):
        strategy = VipUserDiscount()
        # Compra < $30.000 -> 25% desc ($5.000 sobre $20.000)
        self.assertEqual(strategy.calculate_discount(20000.0), 5000.0)
        # Compra >= $30.000 -> 25% desc + $1000 regalado (25% de 40000 = 10000 + 1000 = 11000)
        self.assertEqual(strategy.calculate_discount(40000.0), 11000.0)


class TestOrderCalculatorContext(unittest.TestCase):
    """Pruebas unitarias para el Contexto y el comportamiento dinámico del patrón."""

    def test_context_dynamic_strategy_switching(self):
        calculator = OrderCalculator()
        
        # Seteamos Correo Argentino + Regular
        calculator.shipping_strategy = CorreoArgentinoShipping()
        calculator.discount_strategy = RegularUserDiscount()

        res1 = calculator.calculate_order(subtotal=10000.0, weight_kg=1.0, distance_km=10.0)
        self.assertEqual(res1['discount_amount'], 0.0)
        self.assertEqual(res1['shipping_cost'], 1630.0)  # Base 1200 + 350 + 80

        # Cambiamos dinámicamente las estrategias en runtime (sin instanciar un nuevo contexto)
        calculator.shipping_strategy = AndreaniShipping()
        calculator.discount_strategy = VipUserDiscount()

        res2 = calculator.calculate_order(subtotal=40000.0, weight_kg=1.0, distance_km=10.0)
        # VIP: 25% de 40000 = 10000 + 1000 = 11000
        self.assertEqual(res2['discount_amount'], 11000.0)
        # Andreani: Base 2500 + Tier1 500 + 10km*12 (120) = 3120.0
        self.assertEqual(res2['shipping_cost'], 3120.0)
        self.assertEqual(res2['total_amount'], (40000 - 11000) + 3120.0)

    def test_context_raises_error_without_strategies(self):
        calculator = OrderCalculator()
        with self.assertRaises(RuntimeError):
            calculator.calculate_order(subtotal=10000.0, weight_kg=1.0, distance_km=10.0)


if __name__ == "__main__":
    unittest.main()
