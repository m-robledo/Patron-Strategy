// Implementación en JavaScript del Patrón Strategy para la vista Web (Google Maps)

// 1. Interfaces y Estrategias de Transporte (IRouteStrategy)
const TransportStrategies = {
    car: {
        name: "Automóvil (Vías Rápidas / Autopista)",
        icon: "🚗",
        calculate: (origin, dest, dist) => {
            const duration = (dist / 60) * 60; // 60 km/h
            const fuelCost = dist * 180;
            const toll = dist > 10 ? 800 : 0;
            return {
                durationMinutes: duration,
                costARS: fuelCost + toll,
                calories: dist * 2,
                co2Saved: 0,
                steps: 0,
                waypoints: [
                    `Salida en auto desde ${origin}`,
                    "Incorporación a Autopista / Av. Principal",
                    "Tránsito fluido por carril rápido",
                    `Llegada a ${dest}`
                ]
            };
        },
        code: `class CarRouteStrategy(IRouteStrategy):
    """Estrategia Concreta A: Navegación en Automóvil"""
    def calculate_route(self, origin, destination, distance_km):
        duration_min = (distance_km / 60.0) * 60.0  # 60 km/h
        fuel_cost = distance_km * 180.0
        toll = 800.0 if distance_km > 10.0 else 0.0
        
        return RouteResult(
            transport_name="Automóvil (Vías Rápidas)",
            duration_minutes=round(duration_min, 1),
            monetary_cost_ars=round(fuel_cost + toll, 2),
            calories_burned=distance_km * 2.0,
            co2_saved_kg=0.0,
            estimated_steps=0
        )`
    },
    transit: {
        name: "Transporte Público (Colectivo & Subte)",
        icon: "🚌",
        calculate: (origin, dest, dist) => {
            const duration = ((dist / 25) * 60) + 8; // 25 km/h + 8m espera
            const fare = 450 + (dist * 30);
            return {
                durationMinutes: duration,
                costARS: fare,
                calories: dist * 12,
                co2Saved: dist * 0.14,
                steps: Math.round(dist * 300),
                waypoints: [
                    `Caminata desde ${origin} a parada de colectivo`,
                    "Abordar Línea de Colectivo / Subte (SUBE)",
                    "Recorrido por carril exclusivo METROBUS",
                    `Descenso y caminata final hasta ${dest}`
                ]
            };
        },
        code: `class PublicTransitRouteStrategy(IRouteStrategy):
    """Estrategia Concreta B: Transporte Público"""
    def calculate_route(self, origin, destination, distance_km):
        travel_time = (distance_km / 25.0) * 60.0  # 25 km/h
        waiting_time = 8.0
        sube_fare = 450.0 + (distance_km * 30.0)
        
        return RouteResult(
            transport_name="Transporte Público",
            duration_minutes=round(travel_time + waiting_time, 1),
            monetary_cost_ars=round(sube_fare, 2),
            co2_saved_kg=round(distance_km * 0.14, 2),
            estimated_steps=int(distance_km * 300)
        )`
    },
    bike: {
        name: "Bicicleta (Red de Ciclovías / Bicisendas)",
        icon: "🚲",
        calculate: (origin, dest, dist) => {
            const duration = (dist / 15) * 60; // 15 km/h
            return {
                durationMinutes: duration,
                costARS: 0,
                calories: dist * 30,
                co2Saved: dist * 0.21,
                steps: 0,
                waypoints: [
                    `Partida en bici desde ${origin}`,
                    "Ingreso a Red Protegida de Ciclovías",
                    "Cruce por parque / zona residencial",
                    `Estacionamiento y llegada a ${dest}`
                ]
            };
        },
        code: `class BicycleRouteStrategy(IRouteStrategy):
    """Estrategia Concreta C: Bicicleta"""
    def calculate_route(self, origin, destination, distance_km):
        duration_min = (distance_km / 15.0) * 60.0  # 15 km/h
        
        return RouteResult(
            transport_name="Bicicleta (Ciclovías)",
            duration_minutes=round(duration_min, 1),
            monetary_cost_ars=0.0,
            calories_burned=distance_km * 30.0,
            co2_saved_kg=round(distance_km * 0.21, 2)
        )`
    },
    walk: {
        name: "A Pie (Caminata / Sendero Peatonal)",
        icon: "🚶",
        calculate: (origin, dest, dist) => {
            const duration = (dist / 5) * 60; // 5 km/h
            return {
                durationMinutes: duration,
                costARS: 0,
                calories: dist * 55,
                co2Saved: dist * 0.21,
                steps: Math.round(dist * 1350),
                waypoints: [
                    `Caminata inicial desde ${origin}`,
                    "Cruce por pasajes peatonales y plazas",
                    "Atajo por zona residencial de contramano",
                    `Llegada a pie a ${dest}`
                ]
            };
        },
        code: `class WalkingRouteStrategy(IRouteStrategy):
    """Estrategia Concreta D: A Pie"""
    def calculate_route(self, origin, destination, distance_km):
        duration_min = (distance_km / 5.0) * 60.0  # 5 km/h
        
        return RouteResult(
            transport_name="A Pie (Peatonal)",
            duration_minutes=round(duration_min, 1),
            monetary_cost_ars=0.0,
            calories_burned=distance_km * 55.0,
            estimated_steps=int(distance_km * 1350)
        )`
    }
};

// 2. Interfaces y Estrategias de Optimización (IOptimizationStrategy)
const OptimizationStrategies = {
    fastest: {
        name: "⚡ Ruta Más Rápida (Menor ETA)",
        apply: (result) => {
            result.durationMinutes *= 0.90; // -10% tiempo
            return result;
        },
        code: `class FastestTimeStrategy(IOptimizationStrategy):
    """Estrategia de Criterio A: Más Rápida"""
    def apply_optimization(self, base_result):
        base_result.duration_minutes = round(base_result.duration_minutes * 0.90, 1)
        base_result.notes += " [Optimizada: Menor ETA]."
        return base_result`
    },
    shortest: {
        name: "📏 Ruta Más Corta (Menor Distancia)",
        apply: (result) => {
            result.distKm *= 0.95; // -5% km
            return result;
        },
        code: `class ShortestDistanceStrategy(IOptimizationStrategy):
    """Estrategia de Criterio B: Más Corta"""
    def apply_optimization(self, base_result):
        base_result.distance_km = round(base_result.distance_km * 0.95, 2)
        base_result.notes += " [Optimizada: Menor Recorrido]."
        return base_result`
    },
    economic: {
        name: "💰 Ruta Económica ($0 Peajes)",
        apply: (result) => {
            if (result.costARS > 800) result.costARS -= 800; // elimina peaje
            return result;
        },
        code: `class EconomicStrategy(IOptimizationStrategy):
    """Estrategia de Criterio C: Económica"""
    def apply_optimization(self, base_result):
        if base_result.monetary_cost_ars > 800.0:
            base_result.monetary_cost_ars -= 800.0
        base_result.notes += " [Optimizada: Ahorro de peajes]."
        return base_result`
    }
};

// 3. Contexto (NavigatorContext)
class NavigatorContext {
    constructor(routeStrategy, optimizationStrategy) {
        this.routeStrategy = routeStrategy;
        this.optimizationStrategy = optimizationStrategy;
    }

    planRoute(origin, dest, dist) {
        // Delegación pura en las estrategias
        let route = this.routeStrategy.calculate(origin, dest, dist);
        route.distKm = dist;
        if (this.optimizationStrategy) {
            route = this.optimizationStrategy.apply(route);
        }
        return route;
    }
}

const contextCode = `class NavigatorContext:
    """EL CONTEXTO DEL PATRÓN STRATEGY (Navegador Google Maps)"""
    def __init__(self, route_strategy=None, optimization_strategy=None):
        self._route_strategy = route_strategy
        self._optimization_strategy = optimization_strategy

    def plan_route(self, origin, destination, distance_km):
        # Delegación pura sin ningún 'if/else' de transportes ni criterios
        base_route = self._route_strategy.calculate_route(origin, destination, distance_km)
        
        if self._optimization_strategy is not None:
            return self._optimization_strategy.apply_optimization(base_route)
            
        return base_route`;

// Formateadores
const formatARS = (amount) => new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(amount);

document.addEventListener('DOMContentLoaded', () => {
    const inputOrigin = document.getElementById('origin');
    const inputDest = document.getElementById('destination');
    const inputDist = document.getElementById('distance');
    const distVal = document.getElementById('dist-val');

    const transportCards = document.querySelectorAll('#transport-options .strategy-card');
    const optCards = document.querySelectorAll('#opt-options .opt-card');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const codeBtns = document.querySelectorAll('.code-btn');

    let selectedTransportKey = 'car';
    let selectedOptKey = 'fastest';
    let activeCodeTab = 'context';

    const updateGPS = () => {
        const origin = inputOrigin.value.trim() || "Origen";
        const dest = inputDest.value.trim() || "Destino";
        const dist = parseFloat(inputDist.value) || 12.5;
        distVal.textContent = `${dist} km`;

        const tStrat = TransportStrategies[selectedTransportKey];
        const oStrat = OptimizationStrategies[selectedOptKey];

        const context = new NavigatorContext(tStrat, oStrat);
        const res = context.planRoute(origin, dest, dist);

        // Update ETA & Metrics
        document.getElementById('eta-value').textContent = `${res.durationMinutes.toFixed(1)} min`;
        document.getElementById('eta-transport-badge').textContent = `${tStrat.icon} ${tStrat.name.split(' ')[0]}`;
        document.getElementById('eta-opt-badge').textContent = oStrat.name;

        document.getElementById('m-dist').textContent = `${res.distKm.toFixed(1)} km`;
        document.getElementById('m-cost').textContent = formatARS(res.costARS);
        document.getElementById('m-cal').textContent = `${Math.round(res.calories)} kcal`;

        if (res.steps > 0) {
            document.getElementById('m-eco').textContent = `${res.steps.toLocaleString('es-AR')} pasos`;
        } else {
            document.getElementById('m-eco').textContent = `${res.co2Saved.toFixed(2)} kg CO₂`;
        }

        // Update Map Icon
        document.getElementById('map-icon').textContent = tStrat.icon;

        // Update Waypoints
        const wpList = document.getElementById('waypoints-list');
        wpList.innerHTML = '';
        res.waypoints.forEach(step => {
            const li = document.createElement('li');
            li.textContent = step;
            wpList.appendChild(li);
        });

        // Update UML tags
        document.getElementById('tag-route').textContent = `Estrategia Transporte: ${tStrat.name}`;
        document.getElementById('tag-opt').textContent = `Estrategia Optimización: ${oStrat.name}`;

        updateCodeViewer();
    };

    const updateCodeViewer = () => {
        const codeElement = document.getElementById('code-content');
        if (activeCodeTab === 'context') {
            codeElement.textContent = contextCode;
        } else if (activeCodeTab === 'route') {
            codeElement.textContent = TransportStrategies[selectedTransportKey].code;
        } else if (activeCodeTab === 'opt') {
            codeElement.textContent = OptimizationStrategies[selectedOptKey].code;
        }
    };

    // Selection Transport
    transportCards.forEach(card => {
        card.addEventListener('click', () => {
            transportCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            selectedTransportKey = card.dataset.transport;
            updateGPS();
        });
    });

    // Selection Optimization
    optCards.forEach(card => {
        card.addEventListener('click', () => {
            optCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            selectedOptKey = card.dataset.opt;
            updateGPS();
        });
    });

    // Inputs change
    [inputOrigin, inputDest, inputDist].forEach(input => {
        input.addEventListener('input', updateGPS);
    });

    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
        });
    });

    // Code Tab switching
    codeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            codeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeCodeTab = btn.dataset.code;
            updateCodeViewer();
        });
    });

    // Initial Calculation
    updateGPS();
});
