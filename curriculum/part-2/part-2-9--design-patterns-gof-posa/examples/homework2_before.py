# Starting point for Homework 2 — two things to refactor.
#
# Part A: conditional-heavy dispatch -> refactor into the Strategy pattern.
# Part B: tightly-coupled notification -> refactor into the Observer pattern.
#
# Feel free to translate this to TypeScript/Java/etc. if you prefer; the shape
# of the problem is what matters, not the language.


# --- Part A: refactor this into Strategy ------------------------------------

def calculate_shipping_cost(method: str, weight_kg: float, distance_km: float) -> float:
    if method == "standard":
        return 5.0 + weight_kg * 0.5
    elif method == "express":
        return 12.0 + weight_kg * 0.8 + distance_km * 0.02
    elif method == "overnight":
        return 25.0 + weight_kg * 1.2 + distance_km * 0.05
    elif method == "freight":
        if weight_kg < 50:
            raise ValueError("freight requires at least 50kg")
        return 40.0 + weight_kg * 0.3
    else:
        raise ValueError(f"unknown shipping method: {method}")

# TODO: define a ShippingStrategy interface with a cost(weight_kg, distance_km)
# method, one implementation per branch above, and a registry/factory that
# replaces this function. Adding "international" should mean adding a class.


# --- Part B: refactor this into Observer -------------------------------------

class OrderService:
    def __init__(self, email_client, sms_client, analytics_client, warehouse_client):
        self.email_client = email_client
        self.sms_client = sms_client
        self.analytics_client = analytics_client
        self.warehouse_client = warehouse_client

    def place_order(self, order):
        # ... core order placement logic here ...

        # every interested party is called inline; adding a new one means
        # editing this method, and OrderService must know all four concrete
        # clients directly.
        self.email_client.send_confirmation(order)
        self.sms_client.send_text(order.customer_phone, "Order placed!")
        self.analytics_client.track("order_placed", order.id)
        self.warehouse_client.reserve_stock(order.items)

# TODO: turn OrderService into a Subject that maintains a list of Observers
# (each implementing something like on_order_placed(order)), and turn each
# client above into an Observer implementation registered at startup. Adding
# a fifth interested party should mean registering a new observer, not
# editing place_order.
