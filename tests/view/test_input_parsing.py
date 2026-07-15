from sample_order_system.view.input_parsing import parse_menu_choice, parse_positive_int


def test_유효한_메뉴_선택이면_그대로_반환한다():
    assert parse_menu_choice("2", {"1", "2", "3"}) == "2"


def test_유효하지_않은_메뉴_선택이면_None을_반환한다():
    assert parse_menu_choice("9", {"1", "2", "3"}) is None


def test_양의_정수_문자열이면_정수로_변환한다():
    assert parse_positive_int("200") == 200


def test_숫자가_아니면_None을_반환한다():
    assert parse_positive_int("abc") is None


def test_0_이하의_정수이면_None을_반환한다():
    assert parse_positive_int("0") is None
    assert parse_positive_int("-5") is None
