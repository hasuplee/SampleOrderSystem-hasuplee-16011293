def show_current_job(job) -> None:
    if job is None:
        print("현재 진행 중인 생산 작업이 없습니다.")
        return
    print(
        f"[현재 작업] 주문 {job.order_id}  시료 {job.sample_id}  부족분 {job.shortage_qty}  "
        f"실생산량 {job.actual_qty}  총생산시간 {job.total_time_min:.1f}분"
    )


def show_waiting_queue(jobs) -> None:
    if not jobs:
        print("대기 중인 생산 작업이 없습니다.")
        return
    print("대기 중인 작업 (FIFO 순):")
    for i, job in enumerate(jobs, start=1):
        print(f"  {i}. 주문 {job.order_id}  시료 {job.sample_id}  실생산량 {job.actual_qty}")


def show_message(message: str) -> None:
    print(message)
