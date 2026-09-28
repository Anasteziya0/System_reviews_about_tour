import pytest

import reviews
import tours


@pytest.fixture(autouse=True)
def temp_data_files(tmp_path, monkeypatch):
    """Направить сохранение данных во временные файлы,
    чтобы тесты не изменяли data/*.json."""
    monkeypatch.setattr(tours, "TOURS_FILE", str(tmp_path / "tours.json"))
    monkeypatch.setattr(
        reviews, "REVIEWS_FILE", str(tmp_path / "reviews.json")
    )
