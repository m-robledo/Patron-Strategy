"""
Módulo del Contexto en el Patrón Strategy.

El Contexto (OrderCalculator) mantiene referencias a las estrategias activas
de Envío y Descuento. Delegará en ellas la ejecución de los algoritmos sin
conocer sus implementaciones concretas ni utilizar bloques condicionales (if/else).
"""

from typing import Dict, Any, Optional
from src.strategies.base import IShippingStrategy, IDiscountStrategy


class OrderCalculator:
    """
    Clase Contexto (Context).

    El Contexto define la interfaz de interés para los clientes y mantiene
    una referencia a una o varias instancias de Strategy.
    """

    def __init__(
        self,
        shipping_strategy: Optional[IShippingStrategy] = None,
        discount_strategy: Optional[IDiscountStrategy] = None,
    ):
        """
        Inicializa el Contexto con las estrategias recibidas (inyección de dependencias).
        """
        self._shipping_strategy = shipping_strategy
        self._discount_strategy = discount_strategy

    @property
    def shipping_strategy(self) -> Optional[IShippingStrategy]:
        """Obtiene la estrategia de envío actual."""
        return self._shipping_strategy

    @shipping_strategy.setter
    def shipping_strategy(self, strategy: IShippingStrategy) -> None:
        """
        Permite cambiar dinámicamente la estrategia de envío en tiempo de ejecución.
        """
        if not isinstance(strategy, IShippingStrategy):
            raise TypeError("La estrategia debe implementar IShippingStrategy.")
        self._shipping_strategy = strategy

    @property
    def discount_strategy(self) -> Optional[IDiscountStrategy]:
        """Obtiene la estrategia de descuento actual."""
        return self._discount_strategy

    @discount_strategy.setter
    def discount_strategy(self, strategy: IDiscountStrategy) -> None:
        """
        Permite cambiar dinámicamente la estrategia de descuento en tiempo de ejecución.
        """
        if not isinstance(strategy, IDiscountStrategy):
            raise TypeError("La estrategia debe implementar IDiscountStrategy.")
        self._discount_strategy = strategy

    def calculate_order(
        self, subtotal: float, weight_kg: float, distance_km: float
    ) -> Dict[str, Any]:
        """
        Delega el cálculo a las estrategias configuradas.

        :param subtotal: Precio base de los productos.
        :param weight_kg: Peso total del paquete en kg.
        :param distance_km: Distancia de destino en km.
        :return: Diccionario con el desglose detallado del cálculo.
        """
        if self._shipping_strategy is None:
            raise RuntimeError("No se ha configurado una estrategia de envío.")

        if self._discount_strategy is None:
            raise RuntimeError("No se ha configurado una estrategia de descuento.")

        # 1. Aplicar estrategia de descuento (Delegación)
        discount_amount = self._discount_strategy.calculate_discount(subtotal)
        net_subtotal = max(0.0, subtotal - discount_amount)

        # 2. Aplicar estrategia de envío (Delegación)
        shipping_cost = self._shipping_strategy.calculate(
            weight_kg=weight_kg,
            distance_km=distance_km,
            order_value=subtotal,
        )

        # 3. Calcular total final
        total_amount = net_subtotal + shipping_cost

        return {
            "subtotal": round(subtotal, 2),
            "discount_name": self._discount_strategy.category_name,
            "discount_amount": round(discount_amount, 2),
            "net_subtotal": round(net_subtotal, 2),
            "shipping_name": self._shipping_strategy.name,
            "shipping_cost": round(shipping_cost, 2),
            "total_amount": round(total_amount, 2),
        }
