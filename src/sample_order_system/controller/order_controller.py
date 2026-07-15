from sample_order_system.service.order_service import OrderService
from sample_order_system.view import order_view


class OrderController:
    """시료 주문(예약) 흐름을 담당."""

    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def run(self) -> None:
        data = order_view.get_new_order_input()
        try:
            order = self.order_service.create_order(**data)
            order_view.show_order_confirmation(order)
        except ValueError as e:
            order_view.show_error(str(e))
