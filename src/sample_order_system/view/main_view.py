from sample_order_system.view.prompts import read_menu_choice

_MENU_CHOICES = {"0", "1", "2", "3", "4", "5", "6"}


def show_main_menu(summary: dict) -> None:
    print("=" * 60)
    print("반도체 시료 생산주문관리 시스템")
    print(f"등록 시료 {summary['sample_count']}종   총 재고 {summary['total_stock']} ea")
    print(f"전체 주문 {summary['order_count']}건   생산라인 대기 {summary['producing_count']}건")
    print("-" * 60)
    print("[1] 시료 관리        [2] 시료 주문")
    print("[3] 주문 승인/거절   [4] 모니터링")
    print("[5] 생산라인 조회    [6] 출고 처리")
    print("[0] 종료")


def get_menu_choice() -> str:
    return read_menu_choice("선택 > ", _MENU_CHOICES)


def show_message(message: str) -> None:
    print(message)
