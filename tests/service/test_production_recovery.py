from sample_order_system.model.production_job import ProductionJob
from sample_order_system.model.production_queue import ProductionQueue
from sample_order_system.repository.production_job_repository import ProductionJobRepository
from sample_order_system.service.production_recovery import restore_production_queue


def _작업(order_id):
    return ProductionJob(
        order_id=order_id,
        sample_id="S-001",
        shortage_qty=50,
        actual_qty=72,
        total_time_min=36.0,
    )


def test_저장소에_남아있는_생산_작업을_큐로_복원한다(tmp_db_path):
    job_repo = ProductionJobRepository(tmp_db_path)
    job_repo.create(_작업("ORD-0001"))
    job_repo.create(_작업("ORD-0002"))
    queue = ProductionQueue()

    restore_production_queue(job_repo, queue)

    assert queue.dequeue().order_id == "ORD-0001"
    assert queue.dequeue().order_id == "ORD-0002"


def test_저장소가_비어있으면_큐는_비어있는_상태로_유지된다(tmp_db_path):
    job_repo = ProductionJobRepository(tmp_db_path)
    queue = ProductionQueue()

    restore_production_queue(job_repo, queue)

    assert queue.peek() is None
