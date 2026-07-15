from sample_order_system.model.production_job import ProductionJob
from sample_order_system.model.production_queue import ProductionQueue


def _작업(order_id="ORD-0001"):
    return ProductionJob(
        order_id=order_id,
        sample_id="S-001",
        shortage_qty=20,
        actual_qty=22,
        total_time_min=11.0,
    )


def test_생산_큐는_등록한_순서대로_작업을_반환한다():
    queue = ProductionQueue()
    first = _작업("ORD-0001")
    second = _작업("ORD-0002")

    queue.enqueue(first)
    queue.enqueue(second)

    assert queue.dequeue() == first
    assert queue.dequeue() == second


def test_빈_생산_큐에서_dequeue하면_None을_반환한다():
    queue = ProductionQueue()

    assert queue.dequeue() is None


def test_peek은_큐를_변경하지_않고_첫_작업을_반환한다():
    queue = ProductionQueue()
    job = _작업()
    queue.enqueue(job)

    assert queue.peek() == job
    assert queue.peek() == job
    assert queue.dequeue() == job
