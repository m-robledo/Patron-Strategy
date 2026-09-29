"""
Módulo de Estrategias Concretas de Transporte (Ruta).

Implementa las 4 opciones de navegación estilo Google Maps:
1. Auto (Estrategia Concreta A)
2. Transporte Público / Colectivo & Subte (Estrategia Concreta B)
3. Bicicleta (Estrategia Concreta C)
4. A Pie / Peatonal (Estrategia Concreta D)
"""

from src.strategies.base import IRouteStrategy, RouteResult


class CarRouteStrategy(IRouteStrategy):
    """
    Estrategia Concreta A: Navegación en Automóvil.

    Algoritmo:
    - Velocidad promedio: 60 km/h (Uso de autopistas y avenidas rápidas).
    - Duración: (distancia / 60) * 60 minutos.
    - Costo monetario: Consumo de combustible ($180 ARS/km) + Peaje ($800 ARS si dist > 10km).
    - Emisiones: Emite CO2 (0.0 kg ahorrados).
    """

    @property
    def transport_type(self) -> str:
        return "Automóvil (Vías Rápidas / Autopista)"

    @property
    def icon(self) -> str:
        return "🚗"

    def calculate_route(self, origin: str, destination: str, distance_km: float) -> RouteResult:
        if distance_km <= 0:
            raise ValueError("La distancia debe ser mayor a 0 km.")

        duration_min = (distance_km / 60.0) * 60.0
        fuel_cost = distance_km * 180.0
        toll_cost = 800.0 if distance_km > 10.0 else 0.0
        total_cost = fuel_cost + toll_cost

        waypoints = [
            f"Salida desde {origin}",
            "Incorporación a Av. Principal / Autopista",
            "Tránsito fluido por carril rápido",
            f"Llegada a {destination}"
        ]

        return RouteResult(
            transport_name=self.transport_type,
            distance_km=round(distance_km, 2),
            duration_minutes=round(duration_min, 1),
            monetary_cost_ars=round(total_cost, 2),
            calories_burned=round(distance_km * 2.0, 1),
            co2_saved_kg=0.0,
            estimated_steps=0,
            waypoints=waypoints,
            notes="Ruta optimizada para motor de combustión. Incluye estimación de combustible y peajes."
        )


class PublicTransitRouteStrategy(IRouteStrategy):
    """
    Estrategia Concreta B: Transporte Público (Colectivo / Subte).

    Algoritmo:
    - Velocidad promedio: 25 km/h (contempla paradas, semáforos y espera en estación).
    - Duración: (distancia / 25) * 60 + 8 min de tiempo promedio de espera.
    - Costo monetario: Tarifa SUBE ($450 ARS base + $30 ARS/km).
    - Reducción de CO2: Ahorra ~0.14 kg CO2/km comparado con viajar solo en auto.
    """

    @property
    def transport_type(self) -> str:
        return "Transporte Público (Colectivo & Subte)"

    @property
    def icon(self) -> str:
        return "🚌"

    def calculate_route(self, origin: str, destination: str, distance_km: float) -> RouteResult:
        if distance_km <= 0:
            raise ValueError("La distancia debe ser mayor a 0 km.")

        travel_time = (distance_km / 25.0) * 60.0
        waiting_time = 8.0  # Minutos promedio de frecuencia
        duration_min = travel_time + waiting_time

        sube_fare = 450.0 + (distance_km * 30.0)
        co2_saved = distance_km * 0.14
        walking_steps = int(distance_km * 300)  # Caminata breve a la parada

        waypoints = [
            f"Caminar desde {origin} hasta parada de colectivo (200m)",
            "Abordar Línea de Colectivo / Subte",
            "Recorrido por carril exclusivo METROBUS",
            f"Descenso y caminata final hasta {destination}"
        ]

        return RouteResult(
            transport_name=self.transport_type,
            distance_km=round(distance_km, 2),
            duration_minutes=round(duration_min, 1),
            monetary_cost_ars=round(sube_fare, 2),
            calories_burned=round(distance_km * 12.0, 1),
            co2_saved_kg=round(co2_saved, 2),
            estimated_steps=walking_steps,
            waypoints=waypoints,
            notes="Utiliza red de transporte público urbano. Tarifa calculada con tarjeta SUBE."
        )


class BicycleRouteStrategy(IRouteStrategy):
    """
    Estrategia Concreta C: Bicicleta (Ciclovías / Bicisendas).

    Algoritmo:
    - Velocidad promedio: 15 km/h.
    - Duración: (distancia / 15) * 60 minutos.
    - Costo monetario: $0 ARS.
    - Salud & Ecología: ~30 kcal/km quemadas y 0.21 kg CO2/km ahorrados.
    """

    @property
    def transport_type(self) -> str:
        return "Bicicleta (Red de Ciclovías / Bicisendas)"

    @property
    def icon(self) -> str:
        return "🚲"

    def calculate_route(self, origin: str, destination: str, distance_km: float) -> RouteResult:
        if distance_km <= 0:
            raise ValueError("La distancia debe ser mayor a 0 km.")

        duration_min = (distance_km / 15.0) * 60.0
        calories = distance_km * 30.0
        co2_saved = distance_km * 0.21

        waypoints = [
            f"Partida en bici desde {origin}",
            "Ingreso a Red Protegida de Ciclovías",
            "Cruce por parque / zona de baja velocidad",
            f"Estacionamiento y llegada a {destination}"
        ]

        return RouteResult(
            transport_name=self.transport_type,
            distance_km=round(distance_km, 2),
            duration_minutes=round(duration_min, 1),
            monetary_cost_ars=0.0,
            calories_burned=round(calories, 1),
            co2_saved_kg=round(co2_saved, 2),
            estimated_steps=0,
            waypoints=waypoints,
            notes="Opción sustentable y saludable. Prioriza avenidas con ciclovía delimitada."
        )


class WalkingRouteStrategy(IRouteStrategy):
    """
    Estrategia Concreta D: A Pie (Peatonal).

    Algoritmo:
    - Velocidad promedio: 5 km/h.
    - Duración: (distancia / 5) * 60 minutos.
    - Costo monetario: $0 ARS.
    - Salud & Pasos: ~1350 pasos/km, ~55 kcal/km quemadas y 0.21 kg CO2/km ahorrados.
    """

    @property
    def transport_type(self) -> str:
        return "A Pie (Caminata / Sendero Peatonal)"

    @property
    def icon(self) -> str:
        return "🚶"

    def calculate_route(self, origin: str, destination: str, distance_km: float) -> RouteResult:
        if distance_km <= 0:
            raise ValueError("La distancia debe ser mayor a 0 km.")

        duration_min = (distance_km / 5.0) * 60.0
        calories = distance_km * 55.0
        co2_saved = distance_km * 0.21
        steps = int(distance_km * 1350)

        waypoints = [
            f"Caminata inicial desde {origin}",
            "Cruce por pasajes peatonales y plazas",
            "Atajo por zona residencial / peatonal",
            f"Llegada a pie a {destination}"
        ]

        return RouteResult(
            transport_name=self.transport_type,
            distance_km=round(distance_km, 2),
            duration_minutes=round(duration_min, 1),
            monetary_cost_ars=0.0,
            calories_burned=round(calories, 1),
            co2_saved_kg=round(co2_saved, 2),
            estimated_steps=steps,
            waypoints=waypoints,
            notes="Ruta 100% libre de emisiones y costo cero. Utiliza atajos peatonales de contramano."
        )
