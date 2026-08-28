# Starter skeleton for Homework 1 (CQRS side) — same feature, split into
# a command model (writes, enforces rules) and a query model (reads, shaped
# for display). Compare this file's structure to mvc_order.py.


class ApplyDiscountCommand:
    def __init__(self, order_id: str, percent: float):
        self.order_id = order_id
        self.percent = percent


class OrderCommandHandler:
    """Write side: validates and applies the business rule, persists state."""

    def __init__(self, write_store: dict):
        self.write_store = write_store  # order_id -> order state

    def handle(self, command: ApplyDiscountCommand) -> None:
        # TODO: load order, apply/validate discount rule, save back.
        # This is the ONLY place the discount rule is allowed to live.
        raise NotImplementedError


class OrderSummaryReadModel:
    """Read side: a shape optimized for display, kept in sync separately."""

    def __init__(self, read_store: dict):
        self.read_store = read_store  # order_id -> pre-shaped view dict

    def get_summary(self, order_id: str) -> dict:
        # TODO: return a display-ready dict, no business logic here.
        raise NotImplementedError


# TODO: decide how the read_store gets updated after a command succeeds —
# synchronously in the same call, or via an event the read side subscribes to.
# That decision is the crux of the write-up: document which you chose and why.
