from sample_order_system.service.monitoring_service import MonitoringService
from sample_order_system.view import monitoring_view


class MonitoringController:
    """주문 상태/재고 현황 모니터링 흐름을 담당."""

    def __init__(self, monitoring_service: MonitoringService):
        self.monitoring_service = monitoring_service

    def run(self) -> None:
        while True:
            monitoring_view.show_monitoring_menu()
            choice = monitoring_view.get_monitoring_menu_choice()
            if choice == "1":
                monitoring_view.show_status_counts(self.monitoring_service.status_counts())
            elif choice == "2":
                monitoring_view.show_stock_status(self.monitoring_service.stock_states())
            elif choice == "0":
                break
