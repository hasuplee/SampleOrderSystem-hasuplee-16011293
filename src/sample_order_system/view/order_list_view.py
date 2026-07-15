def show_order_list(rows: list[dict], empty_message: str) -> None:
    if not rows:
        print(empty_message)
        return
    for i, row in enumerate(rows, start=1):
        print(
            f"[{i}] {row['order_id']}  {row['customer_name']}  "
            f"{row['sample_name']}  {row['quantity']} ea"
        )
