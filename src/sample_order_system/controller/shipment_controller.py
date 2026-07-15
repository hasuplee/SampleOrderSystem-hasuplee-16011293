from sample_order_system.model.order import OrderStatus
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.service.shipment_service import ShipmentService
from sample_order_system.view import shipment_view


class ShipmentController:
    """출고 처리 흐름을 담당."""

    def __init__(self, shipment_service: ShipmentService, order_repository: OrderRepository):
        self.shipment_service = shipment_service
        self.order_repository = order_repository

    def run(self) -> None:
        confirmed = [o for o in self.order_repository.list_all() if o.status == OrderStatus.CONFIRMED]
        shipment_view.show_confirmed_orders(confirmed)
        if not confirmed:
            return

        index = shipment_view.get_target_order_index(len(confirmed))
        order = confirmed[index - 1]
        try:
            self.shipment_service.release_order(order.order_id)
            shipment_view.show_shipment_result(self.order_repository.get(order.order_id))
        except ValueError as e:
            shipment_view.show_error(str(e))
