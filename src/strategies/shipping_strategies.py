"""
Módulo de Estrategias Concretas de Envío.

Implementa las tres empresas de logística requeridas:
1. Correo Argentino (Estrategia Concreta A)
2. Andreani (Estrategia Concreta B)
3. PedidosYa (Estrategia Concreta C)
"""

from src.strategies.base import IShippingStrategy


class CorreoArgentinoShipping(IShippingStrategy):
    """
    Estrategia Concreta A: Correo Argentino.

    Servicio postal tradicional y económico a nivel nacional.
    Algoritmo:
    - Tarifa base fija: $1,200 ARS.
    - $350 ARS por kilogramo.
    - $8 ARS por kilómetro.
    - Bonificación: 50% de descuento en el envío si la orden supera los $50,000 ARS.
    """

    BASE_FEE = 1200.0
    PRICE_PER_KG = 350.0
    PRICE_PER_KM = 8.0
    BONUS_THRESHOLD = 50000.0

    @property
    def name(self) -> str:
        return "Correo Argentino (Envío Estándar Nacional)"

    def calculate(self, weight_kg: float, distance_km: float, order_value: float) -> float:
        if weight_kg <= 0 or distance_km <= 0:
            raise ValueError("El peso y la distancia deben ser mayores a 0.")

        cost = self.BASE_FEE + (weight_kg * self.PRICE_PER_KG) + (distance_km * self.PRICE_PER_KM)

        # Bonificación si la orden supera el umbral
        if order_value >= self.BONUS_THRESHOLD:
            cost *= 0.50

        return round(cost, 2)


class AndreaniShipping(IShippingStrategy):
    """
    Estrategia Concreta B: Andreani.

    Empresa privada de logística express y seguimiento en tiempo real.
    Algoritmo:
    - Tarifa base fija: $2,500 ARS (incluye seguro de carga).
    - Adicional por tramo de peso:
        - Hasta 5 kg: +$500 ARS
        - De 5.1 a 15 kg: +$1,200 ARS
        - Más de 15 kg: +$2,500 ARS
    - $12 ARS por kilómetro.
    """

    BASE_FEE = 2500.0
    PRICE_PER_KM = 12.0

    @property
    def name(self) -> str:
        return "Andreani (Envío Privado Express)"

    def calculate(self, weight_kg: float, distance_km: float, order_value: float) -> float:
        if weight_kg <= 0 or distance_km <= 0:
            raise ValueError("El peso y la distancia deben ser mayores a 0.")

        # Tramo por peso
        if weight_kg <= 5.0:
            weight_tier_fee = 500.0
        elif weight_kg <= 15.0:
            weight_tier_fee = 1200.0
        else:
            weight_tier_fee = 2500.0

        cost = self.BASE_FEE + weight_tier_fee + (distance_km * self.PRICE_PER_KM)
        return round(cost, 2)


class PedidosYaShipping(IShippingStrategy):
    """
    Estrategia Concreta C: PedidosYa.

    Servicio de entrega inmediata de última milla (Urbano).
    Algoritmo:
    - Diseñado para envíos cortos (radio máximo: 15 km).
    - Tarifa base urbana: $800 ARS.
    - $150 ARS por kilómetro recorrido.
    - Recargo por peso pesado (si el paquete pesa más de 5 kg, +$600 ARS de comisión del rider).
    - Límite de cobertura: Si la distancia supera los 15 km, lanza una excepción de radio fuera de rango.
    """

    MAX_DISTANCE_KM = 15.0
    BASE_FEE = 800.0
    PRICE_PER_KM = 150.0
    HEAVY_SURCHARGE = 600.0

    @property
    def name(self) -> str:
        return "PedidosYa (Entrega Inmediata Urbana)"

    def calculate(self, weight_kg: float, distance_km: float, order_value: float) -> float:
        if weight_kg <= 0 or distance_km <= 0:
            raise ValueError("El peso y la distancia deben ser mayores a 0.")

        if distance_km > self.MAX_DISTANCE_KM:
            raise ValueError(
                f"PedidosYa solo opera en entregas urbanas de hasta {self.MAX_DISTANCE_KM} km. "
                f"Distancia ingresada: {distance_km} km."
            )

        cost = self.BASE_FEE + (distance_km * self.PRICE_PER_KM)
        if weight_kg > 5.0:
            cost += self.HEAVY_SURCHARGE

        return round(cost, 2)
