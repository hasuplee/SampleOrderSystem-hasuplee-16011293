from sample_order_system.model.production_queue import ProductionQueue
from sample_order_system.repository.production_job_repository import ProductionJobRepository


def restore_production_queue(
    production_job_repository: ProductionJobRepository,
    production_queue: ProductionQueue,
) -> None:
    """저장소에 남아있는 생산 작업을 등록 순서(FIFO)대로 큐에 복원한다."""
    for job in production_job_repository.list_all():
        production_queue.enqueue(job)
