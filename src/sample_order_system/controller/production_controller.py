from sample_order_system.model.production_queue import ProductionQueue
from sample_order_system.service.production_service import ProductionService
from sample_order_system.view import production_view
from sample_order_system.view.prompts import read_menu_choice


class ProductionController:
    """생산라인 조회 및 생산완료 처리 흐름을 담당."""

    def __init__(self, production_service: ProductionService, production_queue: ProductionQueue):
        self.production_service = production_service
        self.production_queue = production_queue

    def run(self) -> None:
        production_view.show_current_job(self.production_queue.peek())
        production_view.show_waiting_queue(self.production_queue.list_all()[1:])

        if self.production_queue.peek() is None:
            return

        choice = read_menu_choice("[1] 생산완료 처리  [0] 뒤로 > ", {"0", "1"})
        if choice == "1":
            self.production_service.complete_current_job()
            production_view.show_message("생산완료 처리되었습니다.")
