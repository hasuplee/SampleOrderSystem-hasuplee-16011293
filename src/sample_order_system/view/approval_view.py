from sample_order_system.view.order_list_view import show_order_list
from sample_order_system.view.prompts import read_index_in_range, read_menu_choice


def show_pending_orders(pending) -> None:
    show_order_list(pending, "승인 대기 중인 주문이 없습니다.")


def get_target_order_index(count: int) -> int:
    return read_index_in_range("승인/거절할 번호 > ", count)


def show_approval_preview(preview) -> None:
    print("재고 확인 중...")
    if preview.sufficient:
        print("재고 충분.")
        return
    print(
        f"재고 부족. 부족분 {preview.shortage_qty} ea "
        f"(실생산량 {preview.actual_qty} ea / {preview.total_time_min:.1f} min)"
    )


def get_approve_or_reject() -> str:
    return read_menu_choice("[Y] 승인  [N] 거절 > ", {"Y", "N", "y", "n"}).upper()


def show_approval_result(order) -> None:
    print(f"처리 완료. 주문번호 {order.order_id}   상태 {order.status.value}")


def show_error(message: str) -> None:
    print(f"오류: {message}")
