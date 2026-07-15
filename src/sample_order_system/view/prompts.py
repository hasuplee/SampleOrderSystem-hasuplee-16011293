from sample_order_system.view.input_parsing import parse_menu_choice, parse_positive_int


def read_menu_choice(prompt: str, valid_choices: set) -> str:
    while True:
        raw = input(prompt)
        choice = parse_menu_choice(raw, valid_choices)
        if choice is not None:
            return choice
        print("잘못된 선택입니다. 다시 입력해주세요.")


def read_positive_int(prompt: str) -> int:
    while True:
        raw = input(prompt)
        value = parse_positive_int(raw)
        if value is not None:
            return value
        print("올바른 양의 정수를 입력해주세요.")


def read_non_negative_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("올바른 정수를 입력해주세요.")
            continue
        if value >= 0:
            return value
        print("0 이상의 정수를 입력해주세요.")


def read_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("올바른 숫자를 입력해주세요.")


def read_text(prompt: str) -> str:
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("값을 입력해주세요.")


def read_index_in_range(prompt: str, count: int) -> int:
    while True:
        index = read_positive_int(prompt)
        if index <= count:
            return index
        print(f"1 ~ {count} 사이의 번호를 입력해주세요.")
