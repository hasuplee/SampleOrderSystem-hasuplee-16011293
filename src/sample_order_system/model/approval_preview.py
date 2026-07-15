from dataclasses import dataclass


@dataclass
class ApprovalPreview:
    """승인 전 재고 확인 미리보기 결과"""
    sufficient: bool
    shortage_qty: int = 0
    actual_qty: int = 0
    total_time_min: float = 0.0
