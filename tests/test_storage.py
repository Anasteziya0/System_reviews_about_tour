import json

from models import Review, Tour, User
from storage import (
    load_reviews,
    load_tours,
    load_users,
    save_reviews,
    save_tours,
    save_users,
)


def make_data():
    tours = [Tour(1, "Обзорная экскурсия", "Центр", 2000, 3)]
    users = [User(1, "Анна", "anna@example.com")]
    reviews = [Review(1, tours[0], users[0], 5, "Отлично!", "2026-09-20")]
    return tours, users, reviews


def test_tours_round_trip(tmp_path):
    tours, _, _ = make_data()
    path = str(tmp_path / "tours.json")
    save_tours(path, tours)
    loaded = load_tours(path)
    assert isinstance(loaded[0], Tour)
    assert loaded[0].name == "Обзорная экскурсия"
    assert loaded[0].price == 2000


def test_users_round_trip(tmp_path):
    _, users, _ = make_data()
    path = str(tmp_path / "users.json")
    save_users(path, users)
    loaded = load_users(path)
    assert isinstance(loaded[0], User)
    assert loaded[0].email == "anna@example.com"


def test_reviews_saved_as_ids(tmp_path):
    _, _, reviews = make_data()
    path = tmp_path / "reviews.json"
    save_reviews(str(path), reviews)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data[0]["tour_id"] == 1
    assert data[0]["user_id"] == 1
    assert "tour" not in data[0]
    assert "user" not in data[0]


def test_reviews_load_restores_links(tmp_path):
    tours, users, reviews = make_data()
    path = str(tmp_path / "reviews.json")
    save_reviews(path, reviews)
    loaded = load_reviews(path, tours, users)
    assert loaded[0].tour is tours[0]
    assert loaded[0].user is users[0]
    assert loaded[0].rating == 5


def test_load_reviews_skips_unknown_tour(tmp_path):
    tours, users, reviews = make_data()
    reviews[0].tour = Tour(99, "Другая", "Где-то", 1, 1)
    path = str(tmp_path / "reviews.json")
    save_reviews(path, reviews)
    assert load_reviews(path, tours, users) == []


def test_load_missing_file(tmp_path):
    assert load_tours(str(tmp_path / "missing.json")) == []


def test_load_corrupted_file_keeps_backup(tmp_path):
    path = tmp_path / "tours.json"
    path.write_text("{ не json", encoding="utf-8")
    assert load_tours(str(path)) == []
    assert (tmp_path / "tours.json.bak").exists()
