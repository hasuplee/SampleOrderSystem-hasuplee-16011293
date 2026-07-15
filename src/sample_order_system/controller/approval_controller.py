from sample_order_system.model.order import OrderStatus
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.service.approval_service import ApprovalService
from sample_order_system.view import approval_view


class ApprovalController:
    """주문 승인/거절 흐름을 담당."""

    def __init__(self, approval_service: ApprovalService, order_repository: OrderRepository):
        self.approval_service = approval_service
        self.order_repository = order_repository

    def run(self) -> None:
        pending = [o for o in self.order_repository.list_all() if o.status == OrderStatus.RESERVED]
        approval_view.show_pending_orders(pending)
        if not pending:
            return

        index = approval_view.get_target_order_index(len(pending))
        order = pending[index - 1]

        try:
            preview = self.approval_service.preview_approval(order.order_id)
        except ValueError as e:
            approval_view.show_error(str(e))
            return
        approval_view.show_approval_preview(preview)

        decision = approval_view.get_approve_or_reject()

        try:
            if decision == "N":
                self.approval_service.reject_order(order.order_id)
            else:
                self.approval_service.approve_order(order.order_id)
            approval_view.show_approval_result(self.order_repository.get(order.order_id))
        except ValueError as e:
            approval_view.show_error(str(e))
