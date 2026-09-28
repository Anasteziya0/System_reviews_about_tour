from reviews import (
    add_review,
    average_rating,
    check_rating,
    count_by_status,
)


def test_check_rating_valid():
    assert check_rating(5) == "Оценка положительная"
    assert check_rating(3) == "Оценка нейтральная"
    assert check_rating(1) == "Оценка отрицательная"


def test_check_rating_invalid():
    assert "Ошибка" in check_rating(0)
    assert "Ошибка" in check_rating(10)


def test_add_review():
    reviews = []
    add_review(reviews, 1, "Анна", 5, "Отлично!")
    assert len(reviews) == 1
    assert reviews[0]["rating"] == 5


def test_add_review_invalid_rating():
    reviews = []
    result = add_review(reviews, 1, "Анна", 10, "Ошибка")
    assert result is None
    assert len(reviews) == 0


def test_average_rating():
    reviews = [
        {"tour_id": 1, "author": "A", "rating": 5,
         "comment": "", "date": "2026-09-20"},
        {"tour_id": 1, "author": "B", "rating": 3,
         "comment": "", "date": "2026-09-20"},
    ]
    assert average_rating(reviews, 1) == 4.0


def test_count_by_status():
    reviews = [
        {"tour_id": 1, "author": "A", "rating": 5,
         "comment": "", "date": "2026-09-20"},
        {"tour_id": 1, "author": "B", "rating": 3,
         "comment": "", "date": "2026-09-20"},
        {"tour_id": 1, "author": "C", "rating": 1,
         "comment": "", "date": "2026-09-20"},
    ]
    stats = count_by_status(reviews, 1)
    assert stats["положительных"] == 1
    assert stats["нейтральных"] == 1
    assert stats["отрицательных"] == 1