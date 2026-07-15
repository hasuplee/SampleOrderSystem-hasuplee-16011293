import pytest


@pytest.fixture
def tmp_db_path(tmp_path):
    """테스트마다 격리된 임시 SQLite DB 파일 경로를 제공한다."""
    return tmp_path / "test.db"
