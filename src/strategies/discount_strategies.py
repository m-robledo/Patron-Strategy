"""
Módulo de Estrategias Concretas de Descuento por Categoría de Usuario.

Implementa las tres categorías de cliente requeridas:
1. Cliente Regular (Estrategia Concreta A)
2. Cliente Mayorista (Estrategia Concreta B)
3. Cliente VIP (Estrategia Concreta C)
"""

from src.strategies.base import IDiscountStrategy


class RegularUserDiscount(IDiscountStrategy):
    """
    Estrategia Concreta A: Usuario Regular.

    - Descuento estándar: 0%.
    - Bonificación especial: 3% de descuento en compras superiores a $100,000 ARS.
    """

    @property
    def category_name(self) -> str:
        return "Cliente Regular"

    def calculate_discount(self, subtotal: float) -> float:
        if subtotal <= 0:
            return 0.0

        if subtotal >= 100000.0:
            return round(subtotal * 0.03, 2)
        return 0.0


class WholesaleDiscount(IDiscountStrategy):
    """
    Estrategia Concreta B: Usuario Mayorista.

    - Descuento base: 15% sobre el subtotal.
    - Descuento volumen: 20% si el subtotal supera los $80,000 ARS.
    """

    @property
    def category_name(self) -> str:
        return "Cliente Mayorista"

    def calculate_discount(self, subtotal: float) -> float:
        if subtotal <= 0:
            return 0.0

        if subtotal >= 80000.0:
            discount_rate = 0.20
        else:
            discount_rate = 0.15

        return round(subtotal * discount_rate, 2)


class VipUserDiscount(IDiscountStrategy):
    """
    Estrategia Concreta C: Usuario VIP.

    - Descuento exclusivo: 25% fijo sobre el subtotal.
    - Cupón adicional de $1,000 ARS de regalo para compras mayores a $30,000 ARS.
    """

    @property
    def category_name(self) -> str:
        return "Cliente VIP"

    def calculate_discount(self, subtotal: float) -> float:
        if subtotal <= 0:
            return 0.0

        discount = subtotal * 0.25

        if subtotal >= 30000.0:
            discount += 1000.0

        # El descuento no puede superar el valor del subtotal
        return round(min(discount, subtotal), 2)
