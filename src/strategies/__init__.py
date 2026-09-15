"""
Paquete de Estrategias para la Calculadora de Envíos y Descuentos.
"""

from src.strategies.base import IShippingStrategy, IDiscountStrategy
from src.strategies.shipping_strategies import (
    CorreoArgentinoShipping,
    AndreaniShipping,
    PedidosYaShipping,
)
from src.strategies.discount_strategies import (
    RegularUserDiscount,
    WholesaleDiscount,
    VipUserDiscount,
)

__all__ = [
    "IShippingStrategy",
    "IDiscountStrategy",
    "CorreoArgentinoShipping",
    "AndreaniShipping",
    "PedidosYaShipping",
    "RegularUserDiscount",
    "WholesaleDiscount",
    "VipUserDiscount",
]
