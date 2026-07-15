def parse_menu_choice(raw: str, valid_choices: set) -> str | None:
    choice = raw.strip()
    return choice if choice in valid_choices else None


def parse_positive_int(raw: str) -> int | None:
    try:
        value = int(raw.strip())
    except ValueError:
        return None
    return value if value > 0 else None
