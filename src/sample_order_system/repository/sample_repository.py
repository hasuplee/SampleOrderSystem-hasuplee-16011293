from sample_order_system.db.connection import get_connection, init_db
from sample_order_system.model.sample import Sample


class SampleRepository:
    """시료(Sample) 테이블에 대한 CRUD."""

    def __init__(self, db_path):
        self.db_path = db_path
        init_db(db_path)

    def create(self, sample: Sample) -> None:
        conn = get_connection(self.db_path)
        try:
            if self._exists(conn, sample.sample_id):
                raise ValueError(f"이미 존재하는 시료 ID입니다: {sample.sample_id}")
            conn.execute(
                "INSERT INTO samples (sample_id, name, avg_production_time, yield_rate, stock) "
                "VALUES (?, ?, ?, ?, ?)",
                (sample.sample_id, sample.name, sample.avg_production_time,
                 sample.yield_rate, sample.stock),
            )
            conn.commit()
        finally:
            conn.close()

    def get(self, sample_id: str) -> Sample | None:
        conn = get_connection(self.db_path)
        try:
            row = conn.execute(
                "SELECT * FROM samples WHERE sample_id = ?", (sample_id,)
            ).fetchone()
            return self._to_sample(row) if row else None
        finally:
            conn.close()

    def list_all(self) -> list[Sample]:
        conn = get_connection(self.db_path)
        try:
            rows = conn.execute("SELECT * FROM samples ORDER BY sample_id").fetchall()
            return [self._to_sample(row) for row in rows]
        finally:
            conn.close()

    def search(self, keyword: str) -> list[Sample]:
        conn = get_connection(self.db_path)
        try:
            rows = conn.execute(
                "SELECT * FROM samples WHERE name LIKE ? ORDER BY sample_id",
                (f"%{keyword}%",),
            ).fetchall()
            return [self._to_sample(row) for row in rows]
        finally:
            conn.close()

    def update(self, sample: Sample) -> None:
        conn = get_connection(self.db_path)
        try:
            conn.execute(
                "UPDATE samples SET name = ?, avg_production_time = ?, "
                "yield_rate = ?, stock = ? WHERE sample_id = ?",
                (sample.name, sample.avg_production_time, sample.yield_rate,
                 sample.stock, sample.sample_id),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _exists(conn, sample_id: str) -> bool:
        row = conn.execute(
            "SELECT 1 FROM samples WHERE sample_id = ?", (sample_id,)
        ).fetchone()
        return row is not None

    @staticmethod
    def _to_sample(row) -> Sample:
        return Sample(
            sample_id=row["sample_id"],
            name=row["name"],
            avg_production_time=row["avg_production_time"],
            yield_rate=row["yield_rate"],
            stock=row["stock"],
        )
