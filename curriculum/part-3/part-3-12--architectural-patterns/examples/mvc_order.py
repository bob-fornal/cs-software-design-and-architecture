# Starter skeleton for Homework 1 (MVC side) — apply a discount to an order.
# Fill in the business rule and the view rendering; this only sketches the shape.


class Order:
    """Model: owns state and business rules."""

    def __init__(self, total: float):
        self.total = total
        self.discount_applied = False

    def apply_discount(self, percent: float) -> None:
        # TODO: business rule lives here, not in the controller.
        # e.g. validate percent range, compute new total, set discount_applied.
        raise NotImplementedError


class OrderController:
    """Controller: mediates input, calls the model, picks a view."""

    def __init__(self, order: Order):
        self.order = order

    def handle_apply_discount_request(self, percent: float) -> str:
        self.order.apply_discount(percent)
        return render_order_view(self.order)


def render_order_view(order: Order) -> str:
    """View: presentation only, no business logic."""
    # TODO: format order.total / order.discount_applied for display.
    raise NotImplementedError


if __name__ == "__main__":
    controller = OrderController(Order(total=100.0))
    print(controller.handle_apply_discount_request(10))
