"""
Punto de Entrada y Demostración CLI para la Facultad.

Demuestra el funcionamiento del Patrón Strategy intercambiando dinámicamente
algoritmos de Envío y Descuento en el objeto Contexto (OrderCalculator).
"""

import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# Asegurar que los módulos de src se puedan importar
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


def print_banner():
    print("=" * 70)
    print("      DEMOSTRACIÓN DEL PATRÓN STRATEGY (DISEÑO DE SOFTWARE)")
    print("          Calculadora de Envíos y Descuentos - Facultad")
    print("=" * 70)


def run_automated_demo():
    print("\n[ESCENARIO DE DEMOSTRACIÓN AUTOMATIZADA]")
    print("Datos de la Orden de Compra:")
    subtotal = 45000.0  # ARS
    weight_kg = 4.5     # kg
    distance_km = 12.0  # km
    print(f" - Subtotal Productos: ${subtotal:,.2f} ARS")
    print(f" - Peso del Paquete:   {weight_kg} kg")
    print(f" - Distancia Destino:  {distance_km} km\n")

    # Instanciamos el Contexto
    calculator = OrderCalculator()

    # Colección de Estrategias
    shipping_strategies = [
        CorreoArgentinoShipping(),
        AndreaniShipping(),
        PedidosYaShipping(),
    ]

    discount_strategies = [
        RegularUserDiscount(),
        WholesaleDiscount(),
        VipUserDiscount(),
    ]

    print("-" * 70)
    print(f"{'Logística (Envío)':<32} | {'Categoría Cliente':<18} | {'Total Final ($)':<12}")
    print("-" * 70)

    # Probamos combinaciones intercambiando estrategias en tiempo de ejecución
    for shipping in shipping_strategies:
        calculator.shipping_strategy = shipping  # Cambio de Estrategia A
        for discount in discount_strategies:
            calculator.discount_strategy = discount  # Cambio de Estrategia B
            
            res = calculator.calculate_order(subtotal, weight_kg, distance_km)
            print(f"{res['shipping_name'][:30]:<32} | {res['discount_name']:<18} | ${res['total_amount']:>10,.2f}")

    print("-" * 70)
    print("\n-> Observación clave para la presentación:")
    print("   El método OrderCalculator.calculate_order() NUNCA cambió ni necesitó 'if/else'")
    print("   para evaluar qué empresa de envío o categoría de cliente se utilizó.")


def run_interactive_cli():
    print("\n[MODO INTERACTIVO EN CONSOLA]")
    try:
        subtotal = float(input("Ingrese el Subtotal de la compra ($ ARS): "))
        weight_kg = float(input("Ingrese el Peso del paquete (kg): "))
        distance_km = float(input("Ingrese la Distancia de envío (km): "))
    except ValueError:
        print("Error: Por favor ingrese números válidos.")
        return

    print("\n--- Seleccione la Logística de Envío (Estrategia de Envío) ---")
    print("1. Correo Argentino (Económico / Nacional)")
    print("2. Andreani (Privado / Express)")
    print("3. PedidosYa (Urbano / Inmediato <= 15km)")
    ship_choice = input("Opción (1-3): ").strip()

    shipping_map = {
        "1": CorreoArgentinoShipping(),
        "2": AndreaniShipping(),
        "3": PedidosYaShipping(),
    }
    selected_shipping = shipping_map.get(ship_choice, CorreoArgentinoShipping())

    print("\n--- Seleccione la Categoría del Usuario (Estrategia de Descuento) ---")
    print("1. Cliente Regular (Sin descuento / 3% en +$100k)")
    print("2. Cliente Mayorista (15% desc / 20% en +$80k)")
    print("3. Cliente VIP (25% desc + $1,000 en +$30k)")
    disc_choice = input("Opción (1-3): ").strip()

    discount_map = {
        "1": RegularUserDiscount(),
        "2": WholesaleDiscount(),
        "3": VipUserDiscount(),
    }
    selected_discount = discount_map.get(disc_choice, RegularUserDiscount())

    # Inyección de estrategias en el Contexto
    context = OrderCalculator(
        shipping_strategy=selected_shipping,
        discount_strategy=selected_discount,
    )

    try:
        result = context.calculate_order(subtotal, weight_kg, distance_km)

        print("\n" + "=" * 50)
        print("          RESULTADO DE LA CALCULADORA")
        print("=" * 50)
        print(f"Subtotal Original:   ${result['subtotal']:>12,.2f} ARS")
        print(f"Descuento ({result['discount_name']}): -${result['discount_amount']:>10,.2f} ARS")
        print(f"Subtotal Neto:       ${result['net_subtotal']:>12,.2f} ARS")
        print(f"Envío ({result['shipping_name']}): +${result['shipping_cost']:>10,.2f} ARS")
        print("-" * 50)
        print(f"TOTAL A PAGAR:       ${result['total_amount']:>12,.2f} ARS")
        print("=" * 50)
    except Exception as e:
        print(f"\n[Error de Ejecución en Estrategia]: {e}")


def launch_web_ui(port=8000):
    web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web"))
    os.chdir(web_dir)
    
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("localhost", port), handler)
    
    url = f"http://localhost:{port}"
    print(f"\n[+] Servidor Web iniciado en {url}")
    print("    Abriendo el navegador para la presentación visual...")
    
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    webbrowser.open(url)


def main():
    print_banner()
    while True:
        print("\nMenú Principal:")
        print("1. Ejecutar Demostración Automatizada (Matriz de Estrategias)")
        print("2. Ejecutar Simulación Interactiva (CLI)")
        print("3. Abrir Interfaz Gráfica Web para la Presentación")
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
