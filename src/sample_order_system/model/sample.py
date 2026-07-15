from dataclasses import dataclass


@dataclass
class Sample:
    """시료(Sample) 데이터 모델"""
    sample_id: str
    name: str
    avg_production_time: float  # min/ea
    yield_rate: float           # 0.0 ~ 1.0
    stock: int = 0
