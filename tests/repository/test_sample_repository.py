import pytest

from sample_order_system.model.sample import Sample
from sample_order_system.repository.sample_repository import SampleRepository


def _시료(sample_id="S-001", name="실리콘 웨이퍼-8인치", avg_production_time=0.5,
        yield_rate=0.92, stock=100):
    return Sample(
        sample_id=sample_id,
        name=name,
        avg_production_time=avg_production_time,
        yield_rate=yield_rate,
        stock=stock,
    )


def test_시료를_등록하면_저장된다(tmp_db_path):
    repo = SampleRepository(tmp_db_path)
    sample = _시료()

    repo.create(sample)
    found = repo.get("S-001")

    assert found == sample


def test_존재하지_않는_시료_ID를_조회하면_None을_반환한다(tmp_db_path):
    repo = SampleRepository(tmp_db_path)

    assert repo.get("S-NOT-EXIST") is None


def test_중복된_시료_ID로_등록하면_예외가_발생한다(tmp_db_path):
    repo = SampleRepository(tmp_db_path)
    repo.create(_시료(sample_id="S-001"))

    with pytest.raises(ValueError):
        repo.create(_시료(sample_id="S-001", name="다른 이름"))


def test_등록된_시료_목록을_조회할_수_있다(tmp_db_path):
    repo = SampleRepository(tmp_db_path)
    repo.create(_시료(sample_id="S-002", name="GaN 에피택셜-4인치"))
    repo.create(_시료(sample_id="S-001", name="실리콘 웨이퍼-8인치"))

    result = repo.list_all()

    assert [s.sample_id for s in result] == ["S-001", "S-002"]


def test_이름으로_시료를_검색하면_부분일치하는_시료만_반환된다(tmp_db_path):
    repo = SampleRepository(tmp_db_path)
    repo.create(_시료(sample_id="S-001", name="실리콘 웨이퍼-8인치"))
    repo.create(_시료(sample_id="S-002", name="GaN 에피택셜-4인치"))

    result = repo.search("실리콘")

    assert [s.sample_id for s in result] == ["S-001"]
