"""
Punto de Entrada y Demostración CLI para la Facultad (Google Maps / Navegación).

Demuestra el funcionamiento del Patrón Strategy intercambiando dinámicamente
medios de transporte y criterios de optimización en el Navegador (NavigatorContext).
"""

import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# Asegurar que los módulos de src se puedan importar
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


def print_banner():
    print("=" * 75)
    print("       PLANIFICADOR DE RUTAS ESTILO GOOGLE MAPS - PATRÓN STRATEGY")
    print("               Demostración para la Facultad / Universidad")
    print("=" * 75)


def run_automated_demo():
    print("\n[ESCENARIO DE DEMOSTRACIÓN AUTOMATIZADA]")
    origin = "Obelisco, CABA"
    destination = "Ciudad Universitaria, UBA"
    distance_km = 12.5

    print(f"Origen:      {origin}")
    print(f"Destino:     {destination}")
    print(f"Distancia:   {distance_km} km\n")

    navigator = NavigatorContext()

    transport_strategies = [
        CarRouteStrategy(),
        PublicTransitRouteStrategy(),
        BicycleRouteStrategy(),
        WalkingRouteStrategy(),
    ]

    optimization_strategies = [
        FastestTimeStrategy(),
        ShortestDistanceStrategy(),
        EconomicStrategy(),
    ]

    print("-" * 75)
    print(f"{'Medio de Transporte':<35} | {'Criterio':<22} | {'Duración (ETA)':<12}")
    print("-" * 75)

    for transport in transport_strategies:
        navigator.route_strategy = transport
        for opt in optimization_strategies:
            navigator.optimization_strategy = opt
            route = navigator.plan_route(origin, destination, distance_km)
            
            label = f"{transport.icon} {transport.transport_type[:28]}"
            print(f"{label:<35} | {opt.criterion_name:<22} | {route.duration_minutes:>6.1f} min")

    print("-" * 75)
    print("\n-> Observación para la exposición en la facultad:")
    print("   El método NavigatorContext.plan_route() ejecuta el cálculo delegando")
    print("   sin evaluar un solo 'if/else' de transportes ni criterios de optimización.")


def run_interactive_cli():
    print("\n[MODO INTERACTIVO EN CONSOLA]")
    origin = input("Punto de Partida (ej. Centro): ").strip() or "Centro"
    destination = input("Punto de Llegada (ej. Facultad): ").strip() or "Facultad"
    try:
        distance_km = float(input("Distancia en Kilómetros (ej. 8.5): ") or "8.5")
    except ValueError:
        print("Error: Ingrese una distancia numérica válida.")
        return

    print("\n--- Seleccione el Medio de Transporte (Estrategia de Ruta) ---")
    print("1. 🚗 Automóvil (Autopista / Combustible + Peajes)")
    print("2. 🚌 Transporte Público (Colectivo / Subte / Tarjeta SUBE)")
    print("3. 🚲 Bicicleta (Red de Ciclovías / $0 costo / Saludable)")
    print("4. 🚶 A Pie (Peatonal / $0 costo / Contador de pasos)")
    t_choice = input("Opción (1-4): ").strip()

    t_map = {
        "1": CarRouteStrategy(),
        "2": PublicTransitRouteStrategy(),
        "3": BicycleRouteStrategy(),
        "4": WalkingRouteStrategy(),
    }
    selected_transport = t_map.get(t_choice, CarRouteStrategy())

    print("\n--- Seleccione el Criterio (Estrategia de Optimización) ---")
    print("1. ⚡ Ruta Más Rápida (Menor Tiempo)")
    print("2. 📏 Ruta Más Corta (Menor Distancia)")
    print("3. 💰 Ruta Económica (Ahorro Monetario)")
    o_choice = input("Opción (1-3): ").strip()

    o_map = {
        "1": FastestTimeStrategy(),
        "2": ShortestDistanceStrategy(),
        "3": EconomicStrategy(),
    }
    selected_opt = o_map.get(o_choice, FastestTimeStrategy())

    navigator = NavigatorContext(
        route_strategy=selected_transport,
        optimization_strategy=selected_opt,
    )

    try:
        result = navigator.plan_route(origin, destination, distance_km)

        print("\n" + "=" * 60)
        print(f"        ITINERARIO CALCULADO POR EL NAVEGADOR")
        print("=" * 60)
        print(f"Transporte:       {selected_transport.icon} {result.transport_name}")
        print(f"Criterio:         {selected_opt.criterion_name}")
        print(f"Distancia Total:  {result.distance_km} km")
        print(f"Duración (ETA):   {result.duration_minutes} minutos")
        print(f"Costo Monetario:  ${result.monetary_cost_ars:,.2f} ARS")
        print(f"Calorías:         {result.calories_burned} kcal")
        print(f"CO2 Ahorrado:     {result.co2_saved_kg} kg CO2")
        print(f"Pasos Estimados:  {result.estimated_steps} pasos")
        print("-" * 60)
        print("Puntos del Trayecto (Waypoints):")
        for i, step in enumerate(result.waypoints, 1):
            print(f"  {i}. {step}")
        print("-" * 60)
        print(f"Notas del GPS:    {result.notes}")
        print("=" * 60)
    except Exception as e:
        print(f"\n[Error de Ejecución]: {e}")


def launch_web_ui(port=8000):
    web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web"))
    os.chdir(web_dir)
    
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("localhost", port), handler)
    
    url = f"http://localhost:{port}"
    print(f"\n[+] Servidor Web GPS iniciado en {url}")
    print("    Abriendo el navegador para la presentación visual estilo Google Maps...")
    
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    webbrowser.open(url)


def main():
    print_banner()
    while True:
        print("\nMenú Principal:")
        print("1. Demostración Automatizada (Matriz de Transportes y Criterios)")
        print("2. Simulación Interactiva por Consola (CLI)")
        print("3. Abrir Interfaz Gráfica Web GPS para la Presentación")
        print("4. Salir")
        
        choice = input("\nSeleccione una opción (1-4): ").strip()
        if choice == "1":
            run_automated_demo()
        elif choice == "2":
            run_interactive_cli()
        elif choice == "3":
            launch_web_ui()
        elif choice == "4":
            print("\n¡Gracias por utilizar la demostración del Patrón Strategy!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
