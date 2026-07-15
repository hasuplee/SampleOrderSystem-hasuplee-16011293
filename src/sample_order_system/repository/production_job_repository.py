from sample_order_system.db.connection import get_connection, init_db
from sample_order_system.model.production_job import ProductionJob


class ProductionJobRepository:
    """생산 작업(ProductionJob) 테이블에 대한 CRUD."""

    def __init__(self, db_path):
        self.db_path = db_path
        init_db(db_path)

    def create(self, job: ProductionJob) -> None:
        conn = get_connection(self.db_path)
        try:
            conn.execute(
                "INSERT INTO production_jobs "
                "(order_id, sample_id, shortage_qty, actual_qty, total_time_min) "
                "VALUES (?, ?, ?, ?, ?)",
                (job.order_id, job.sample_id, job.shortage_qty, job.actual_qty,
                 job.total_time_min),
            )
            conn.commit()
        finally:
            conn.close()

    def list_all(self) -> list[ProductionJob]:
        conn = get_connection(self.db_path)
        try:
            rows = conn.execute("SELECT * FROM production_jobs ORDER BY id").fetchall()
            return [self._to_job(row) for row in rows]
        finally:
            conn.close()

    def delete(self, order_id: str) -> None:
        conn = get_connection(self.db_path)
        try:
            conn.execute("DELETE FROM production_jobs WHERE order_id = ?", (order_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _to_job(row) -> ProductionJob:
        return ProductionJob(
            order_id=row["order_id"],
            sample_id=row["sample_id"],
            shortage_qty=row["shortage_qty"],
            actual_qty=row["actual_qty"],
            total_time_min=row["total_time_min"],
        )
