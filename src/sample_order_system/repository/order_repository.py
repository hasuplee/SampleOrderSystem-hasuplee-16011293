import re

from sample_order_system.db.connection import get_connection, init_db
from sample_order_system.model.order import Order, OrderStatus

_ORDER_ID_PATTERN = re.compile(r"^ORD-(\d+)$")


class OrderRepository:
    """주문(Order) 테이블에 대한 CRUD."""

    def __init__(self, db_path):
        self.db_path = db_path
        init_db(db_path)

    def create(self, order: Order) -> None:
        conn = get_connection(self.db_path)
        try:
            conn.execute(
                "INSERT INTO orders (order_id, sample_id, customer_name, quantity, status) "
                "VALUES (?, ?, ?, ?, ?)",
                (order.order_id, order.sample_id, order.customer_name,
                 order.quantity, order.status.value),
            )
            conn.commit()
        finally:
            conn.close()

    def get(self, order_id: str) -> Order | None:
        conn = get_connection(self.db_path)
        try:
            row = conn.execute(
                "SELECT * FROM orders WHERE order_id = ?", (order_id,)
            ).fetchone()
            return self._to_order(row) if row else None
        finally:
            conn.close()

    def next_order_id(self) -> str:
        """기존 주문 ID(ORD-####) 중 최댓값 다음 번호를 ORD-#### 형식으로 반환한다."""
        conn = get_connection(self.db_path)
        try:
            rows = conn.execute("SELECT order_id FROM orders").fetchall()
        finally:
            conn.close()

        max_num = 0
        for row in rows:
            m = _ORDER_ID_PATTERN.match(row["order_id"])
            if m:
                max_num = max(max_num, int(m.group(1)))
        return f"ORD-{max_num + 1:04d}"

    def update(self, order: Order) -> None:
        conn = get_connection(self.db_path)
        try:
            conn.execute(
                "UPDATE orders SET sample_id = ?, customer_name = ?, "
                "quantity = ?, status = ? WHERE order_id = ?",
                (order.sample_id, order.customer_name, order.quantity,
                 order.status.value, order.order_id),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _to_order(row) -> Order:
        return Order(
            order_id=row["order_id"],
            sample_id=row["sample_id"],
            customer_name=row["customer_name"],
            quantity=row["quantity"],
            status=OrderStatus(row["status"]),
        )
