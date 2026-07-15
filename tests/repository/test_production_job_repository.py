from sample_order_system.model.production_job import ProductionJob
from sample_order_system.repository.production_job_repository import ProductionJobRepository


def _작업(order_id):
    return ProductionJob(
        order_id=order_id,
        sample_id="S-001",
        shortage_qty=50,
        actual_qty=72,
        total_time_min=36.0,
    )


def test_생산_작업을_등록하면_저장된다(tmp_db_path):
    repo = ProductionJobRepository(tmp_db_path)
    job = _작업("ORD-0001")

    repo.create(job)

    assert repo.list_all() == [job]


def test_생산_작업을_삭제하면_목록에서_사라진다(tmp_db_path):
    repo = ProductionJobRepository(tmp_db_path)
    job = _작업("ORD-0001")
    repo.create(job)

    repo.delete(job.order_id)

    assert repo.list_all() == []


def test_여러_작업을_등록하면_등록_순서대로_조회된다(tmp_db_path):
    repo = ProductionJobRepository(tmp_db_path)
    first = _작업("ORD-0002")
    second = _작업("ORD-0001")

    repo.create(first)
    repo.create(second)

    assert [job.order_id for job in repo.list_all()] == ["ORD-0002", "ORD-0001"]
