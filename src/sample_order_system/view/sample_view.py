from sample_order_system.view.prompts import (
    read_float,
    read_menu_choice,
    read_non_negative_int,
    read_text,
)

_MENU_CHOICES = {"0", "1", "2", "3"}


def show_sample_menu() -> None:
    print("[1] 시료 등록  [2] 시료 목록  [3] 시료 검색  [0] 뒤로")


def get_sample_menu_choice() -> str:
    return read_menu_choice("선택 > ", _MENU_CHOICES)


def get_new_sample_input() -> dict:
    return {
        "sample_id": read_text("시료 ID > "),
        "name": read_text("이름 > "),
        "avg_production_time": read_float("평균 생산시간(min/ea) > "),
        "yield_rate": read_float("수율(0.0~1.0) > "),
        "stock": read_non_negative_int("초기 재고 > "),
    }


def show_sample_list(samples) -> None:
    if not samples:
        print("등록된 시료가 없습니다.")
        return
    for sample in samples:
        print(f"{sample.sample_id}\t{sample.name}\t재고 {sample.stock} ea")


def get_search_keyword() -> str:
    return read_text("검색어 > ")


def show_search_result(result) -> None:
    show_sample_list(result)


def show_error(message: str) -> None:
    print(f"오류: {message}")
