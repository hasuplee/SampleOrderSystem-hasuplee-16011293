from sample_order_system.model.production_job import ProductionJob


class ProductionQueue:
    """생산 라인의 FIFO 대기열을 표현하는 모델"""

    def __init__(self):
        self._jobs: list[ProductionJob] = []

    def enqueue(self, job: ProductionJob) -> None:
        self._jobs.append(job)

    def dequeue(self) -> ProductionJob | None:
        return self._jobs.pop(0) if self._jobs else None

    def peek(self) -> ProductionJob | None:
        return self._jobs[0] if self._jobs else None

    def list_all(self) -> list[ProductionJob]:
        return list(self._jobs)
