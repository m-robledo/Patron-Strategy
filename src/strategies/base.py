"""
Módulo de Interfaces Base para el Patrón Strategy.

Define los contratos abstractos (Interfaces en lenguajes orientados a objetos)
que todas las estrategias concretas de envío y descuento deben implementar.
"""

from abc import ABC, abstractmethod


class IShippingStrategy(ABC):
    """
    Interfaz / Abstracción para las Estrategias de Envío (Logística).

    En el patrón Strategy, esta interfaz declara la operación común para
    todos los algoritmos de cálculo de envío soportados.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre descriptivo de la logística."""
        pass

    @abstractmethod
    def calculate(self, weight_kg: float, distance_km: float, order_value: float) -> float:
        """
        Calcula el costo del envío en base a los parámetros proporcionados.

        :param weight_kg: Peso del paquete en kilogramos.
        :param distance_km: Distancia de entrega en kilómetros.
        :param order_value: Valor total de los productos de la compra.
        :return: Costo final del servicio de envío en ARS ($).
        """
        pass


class IDiscountStrategy(ABC):
    """
    Interfaz / Abstracción para las Estrategias de Descuento (Categoría de Usuario).

    Declara el método común para aplicar beneficios o descuentos sobre
    el valor de la orden o subtotal.
    """

    @property
    @abstractmethod
    def category_name(self) -> str:
        """Nombre de la categoría de usuario."""
        pass

    @abstractmethod
    def calculate_discount(self, subtotal: float) -> float:
        """
        Calcula el monto a descontar según la estrategia de descuento.

        :param subtotal: Subtotal de la compra (antes de descuentos).
        :return: Monto descontado en ARS ($).
        """
        pass
