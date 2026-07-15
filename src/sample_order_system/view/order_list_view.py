def show_order_list(orders, empty_message: str) -> None:
    if not orders:
        print(empty_message)
        return
    for i, order in enumerate(orders, start=1):
        print(f"[{i}] {order.order_id}  {order.customer_name}  {order.sample_id}  {order.quantity} ea")
