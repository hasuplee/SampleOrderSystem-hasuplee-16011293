from sample_order_system.controller.approval_controller import ApprovalController
from sample_order_system.controller.monitoring_controller import MonitoringController
from sample_order_system.controller.order_controller import OrderController
from sample_order_system.controller.production_controller import ProductionController
from sample_order_system.controller.sample_controller import SampleController
from sample_order_system.controller.shipment_controller import ShipmentController
from sample_order_system.model.order import OrderStatus
from sample_order_system.view import main_view


class MainController:
    """메인 메뉴를 표시하고 각 하위 Controller로 흐름을 위임."""

    def __init__(
        self,
        sample_repository,
        order_repository,
        order_service,
        approval_service,
        monitoring_service,
        production_service,
        production_queue,
        shipment_service,
    ):
        self.sample_repository = sample_repository
        self.order_repository = order_repository

        self.sample_controller = SampleController(sample_repository)
        self.order_controller = OrderController(order_service)
        self.approval_controller = ApprovalController(approval_service, order_repository)
        self.monitoring_controller = MonitoringController(monitoring_service)
        self.production_controller = ProductionController(production_service, production_queue)
        self.shipment_controller = ShipmentController(shipment_service, order_repository)

    def run(self) -> None:
        while True:
            main_view.show_main_menu(self._build_summary())
            choice = main_view.get_menu_choice()
            if choice == "1":
                self.sample_controller.run()
            elif choice == "2":
                self.order_controller.run()
            elif choice == "3":
                self.approval_controller.run()
            elif choice == "4":
                self.monitoring_controller.run()
            elif choice == "5":
                self.production_controller.run()
            elif choice == "6":
                self.shipment_controller.run()
            elif choice == "0":
                main_view.show_message("시스템을 종료합니다.")
                break

    def _build_summary(self) -> dict:
        orders = self.order_repository.list_all()
        samples = self.sample_repository.list_all()
        producing_count = sum(1 for o in orders if o.status == OrderStatus.PRODUCING)
        return {
            "sample_count": len(samples),
            "total_stock": sum(s.stock for s in samples),
            "order_count": len(orders),
            "producing_count": producing_count,
        }
