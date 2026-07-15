from dataclasses import dataclass


@dataclass
class ProductionJob:
    """생산 큐에 등록되는 생산 작업 데이터 모델"""
    order_id: str
    sample_id: str
    shortage_qty: int      # 부족분 = 주문량 - 재고
    actual_qty: int        # 실생산량 = ceil(부족분 / 수율)
    total_time_min: float  # 총 생산 시간 = 평균 생산시간 * 실생산량
