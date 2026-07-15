from sample_order_system.view.prompts import read_menu_choice

_MENU_CHOICES = {"0", "1", "2"}


def show_monitoring_menu() -> None:
    print("[1] 주문량 확인  [2] 재고량 확인  [0] 뒤로")


def get_monitoring_menu_choice() -> str:
    return read_menu_choice("선택 > ", _MENU_CHOICES)


def show_status_counts(counts: dict) -> None:
    for status, count in counts.items():
        print(f"{status}\t{count}건")


def show_stock_status(rows) -> None:
    if not rows:
        print("등록된 시료가 없습니다.")
        return
    for row in rows:
        print(
            f"{row['sample_id']}\t{row['name']}\t재고 {row['stock']}\t"
            f"대기수요 {row['pending_demand']}\t{row['state']}\t잔여율 {row['ratio']:.0%}"
        )
