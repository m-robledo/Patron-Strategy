// Implementación en JavaScript del Patrón Strategy para la vista Web

// 1. Interfaces y Estrategias de Envío
const ShippingStrategies = {
    correo: {
        name: "Correo Argentino (Envío Estándar Nacional)",
        calculate: (weight, distance, subtotal) => {
            if (weight <= 0 || distance <= 0) throw new Error("Peso y distancia deben ser > 0");
            let cost = 1200 + (weight * 350) + (distance * 8);
            if (subtotal >= 50000) cost *= 0.50; // Bonificación 50%
            return cost;
        },
        code: `class CorreoArgentinoShipping(IShippingStrategy):
    BASE_FEE = 1200.0
    PRICE_PER_KG = 350.0
    PRICE_PER_KM = 8.0

    def calculate(self, weight_kg, distance_km, order_value):
        cost = self.BASE_FEE + (weight_kg * 350) + (distance_km * 8)
        if order_value >= 50000.0:
            cost *= 0.50  # 50% de bonificación
        return round(cost, 2)`
    },
    andreani: {
        name: "Andreani (Envío Privado Express)",
        calculate: (weight, distance, subtotal) => {
            if (weight <= 0 || distance <= 0) throw new Error("Peso y distancia deben ser > 0");
            let tierFee = 500;
            if (weight > 15) tierFee = 2500;
            else if (weight > 5) tierFee = 1200;
            return 2500 + tierFee + (distance * 12);
        },
        code: `class AndreaniShipping(IShippingStrategy):
    BASE_FEE = 2500.0

    def calculate(self, weight_kg, distance_km, order_value):
        if weight_kg <= 5.0: weight_tier = 500.0
        elif weight_kg <= 15.0: weight_tier = 1200.0
        else: weight_tier = 2500.0

        return round(self.BASE_FEE + weight_tier + (distance_km * 12.0), 2)`
    },
    pedidosya: {
        name: "PedidosYa (Entrega Inmediata Urbana)",
        calculate: (weight, distance, subtotal) => {
            if (weight <= 0 || distance <= 0) throw new Error("Peso y distancia deben ser > 0");
            if (distance > 15) {
                throw new Error("PedidosYa solo opera en entregas de hasta 15 km.");
            }
            let cost = 800 + (distance * 150);
            if (weight > 5) cost += 600; // Recargo paquete pesado
            return cost;
        },
        code: `class PedidosYaShipping(IShippingStrategy):
    MAX_DISTANCE = 15.0

    def calculate(self, weight_kg, distance_km, order_value):
        if distance_km > 15.0:
            raise ValueError("Fuera de radio de cobertura urbano (max 15km).")
        
        cost = 800.0 + (distance_km * 150.0)
        if weight_kg > 5.0: cost += 600.0 # Recargo rider
        return round(cost, 2)`
    }
};

// 2. Interfaces y Estrategias de Descuento
const DiscountStrategies = {
    regular: {
        name: "Cliente Regular",
        calculateDiscount: (subtotal) => {
            if (subtotal >= 100000) return subtotal * 0.03;
            return 0;
        },
        code: `class RegularUserDiscount(IDiscountStrategy):
    def calculate_discount(self, subtotal):
        if subtotal >= 100000.0:
            return round(subtotal * 0.03, 2)  # 3% bonificación
        return 0.0`
    },
    wholesale: {
        name: "Cliente Mayorista",
        calculateDiscount: (subtotal) => {
            const rate = subtotal >= 80000 ? 0.20 : 0.15;
            return subtotal * rate;
        },
        code: `class WholesaleDiscount(IDiscountStrategy):
    def calculate_discount(self, subtotal):
        rate = 0.20 if subtotal >= 80000.0 else 0.15
        return round(subtotal * rate, 2)`
    },
    vip: {
        name: "Cliente VIP",
        calculateDiscount: (subtotal) => {
            let desc = subtotal * 0.25;
            if (subtotal >= 30000) desc += 1000;
            return Math.min(desc, subtotal);
        },
        code: `class VipUserDiscount(IDiscountStrategy):
    def calculate_discount(self, subtotal):
        discount = subtotal * 0.25
        if subtotal >= 30000.0:
            discount += 1000.0  # Cupón regalo
        return round(min(discount, subtotal), 2)`
    }
};

// 3. El Contexto (OrderCalculator)
class OrderCalculatorContext {
    constructor(shippingStrategy, discountStrategy) {
        this.shippingStrategy = shippingStrategy;
        this.discountStrategy = discountStrategy;
    }

    calculate(subtotal, weight, distance) {
        const discountAmount = this.discountStrategy.calculateDiscount(subtotal);
        const netSubtotal = Math.max(0, subtotal - discountAmount);
        const shippingCost = this.shippingStrategy.calculate(weight, distance, subtotal);
        const total = netSubtotal + shippingCost;

        return {
            subtotal,
            discountAmount,
            netSubtotal,
            shippingCost,
            total,
            shippingName: this.shippingStrategy.name,
            discountName: this.discountStrategy.name
        };
    }
}

const contextCode = `class OrderCalculator:
    """EL CONTEXTO DEL PATRÓN STRATEGY"""
    def __init__(self, shipping_strategy=None, discount_strategy=None):
        self._shipping_strategy = shipping_strategy
        self._discount_strategy = discount_strategy

    def calculate_order(self, subtotal, weight_kg, distance_km):
        # Delegación pura en las estrategias (¡Sin condicionales!)
        discount = self._discount_strategy.calculate_discount(subtotal)
        net_subtotal = max(0.0, subtotal - discount)
        
        shipping = self._shipping_strategy.calculate(weight_kg, distance_km, subtotal)
        
        return {
            "subtotal": subtotal,
            "discount_amount": discount,
            "net_subtotal": net_subtotal,
            "shipping_cost": shipping,
            "total_amount": net_subtotal + shipping
        }`;

// Formateador de Moneda ARS
const formatARS = (amount) => {
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 2
    }).format(amount);
};

// UI State & Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const inputSubtotal = document.getElementById('subtotal');
    const inputWeight = document.getElementById('weight');
    const inputDistance = document.getElementById('distance');

    const shippingCards = document.querySelectorAll('#shipping-options .strategy-card');
    const discountCards = document.querySelectorAll('#discount-options .strategy-card');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const codeBtns = document.querySelectorAll('.code-btn');

    let selectedShippingKey = 'correo';
    let selectedDiscountKey = 'regular';
    let activeCodeTab = 'context';

    const updateCalculation = () => {
        const subtotal = parseFloat(inputSubtotal.value) || 0;
        const weight = parseFloat(inputWeight.value) || 0;
        const distance = parseFloat(inputDistance.value) || 0;

        const shippingStrat = ShippingStrategies[selectedShippingKey];
        const discountStrat = DiscountStrategies[selectedDiscountKey];

        const context = new OrderCalculatorContext(shippingStrat, discountStrat);

        try {
            const res = context.calculate(subtotal, weight, distance);

            document.getElementById('res-subtotal').textContent = formatARS(res.subtotal);
            document.getElementById('res-discount').textContent = `-${formatARS(res.discountAmount)}`;
            document.getElementById('res-discount-name').textContent = res.discountName;
            document.getElementById('res-net').textContent = formatARS(res.netSubtotal);
            document.getElementById('res-shipping').textContent = `+${formatARS(res.shippingCost)}`;
            document.getElementById('res-shipping-name').textContent = res.shippingName;
            document.getElementById('res-total').textContent = `${formatARS(res.total)} ARS`;

            document.getElementById('tag-ship').textContent = `Estrategia Envío Activa: ${shippingStrat.name}`;
            document.getElementById('tag-disc').textContent = `Estrategia Descuento Activa: ${discountStrat.name}`;

            updateCodeViewer();
        } catch (err) {
            document.getElementById('res-shipping').textContent = "ERROR";
            document.getElementById('res-shipping-name').textContent = err.message;
            document.getElementById('res-total').textContent = "⚠️ REVISAR PARÁMETROS";
        }
    };

    const updateCodeViewer = () => {
        const codeElement = document.getElementById('code-content');
        if (activeCodeTab === 'context') {
            codeElement.textContent = contextCode;
        } else if (activeCodeTab === 'ship') {
            codeElement.textContent = ShippingStrategies[selectedShippingKey].code;
        } else if (activeCodeTab === 'disc') {
            codeElement.textContent = DiscountStrategies[selectedDiscountKey].code;
        }
    };

    // Selection Shipping
    shippingCards.forEach(card => {
        card.addEventListener('click', () => {
            shippingCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            selectedShippingKey = card.dataset.shipping;
            updateCalculation();
        });
    });

    // Selection Discount
    discountCards.forEach(card => {
        card.addEventListener('click', () => {
            discountCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            selectedDiscountKey = card.dataset.discount;
            updateCalculation();
        });
    });

    // Inputs change
    [inputSubtotal, inputWeight, inputDistance].forEach(input => {
        input.addEventListener('input', updateCalculation);
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
    updateCalculation();
});
