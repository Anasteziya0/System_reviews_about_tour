from models import Review, Tour, User
from models.reviews import (
    add_review,
    average_rating,
    check_rating,
    count_by_status,
    get_reviews_for_tour,
)


def make_objects():
    tour = Tour(1, "Обзорная экскурсия", "Центр", 2000, 3)
    other_tour = Tour(2, "Ночная экскурсия", "Набережная", 1500, 2)
    user = User(1, "Анна", "anna@example.com")
    return tour, other_tour, user


def test_review_creation_links_objects():
    tour, _, user = make_objects()
    review = Review(1, tour, user, 5, "Отлично!", "2026-09-20")
    assert review.id == 1
    assert review.tour is tour
    assert review.user is user
    assert review.rating == 5
    assert review.comment == "Отлично!"
    assert review.review_date == "2026-09-20"


def test_review_str():
    tour, _, user = make_objects()
    review = Review(1, tour, user, 5, "Отлично!", "2026-09-20")
    assert str(review) == "Анна (2026-09-20): 5/5 — Отлично!"


def test_review_get_status():
    tour, _, user = make_objects()
    assert Review(1, tour, user, 5, "", "d").get_status() == (
        "Оценка положительная"
    )
    assert Review(2, tour, user, 3, "", "d").get_status() == (
        "Оценка нейтральная"
    )
    assert Review(3, tour, user, 1, "", "d").get_status() == (
        "Оценка отрицательная"
    )


def test_validate_rating():
    assert Review.validate_rating(1)
    assert Review.validate_rating(5)
    assert not Review.validate_rating(0)
    assert not Review.validate_rating(6)


def test_check_rating_valid():
    assert check_rating(5) == "Оценка положительная"
    assert check_rating(3) == "Оценка нейтральная"
    assert check_rating(1) == "Оценка отрицательная"


def test_check_rating_invalid():
    assert "Ошибка" in check_rating(0)
    assert "Ошибка" in check_rating(10)


def test_add_review():
    tour, _, user = make_objects()
    reviews = []
    review = add_review(reviews, tour, user, 5, "Отлично!")
    assert reviews == [review]
    assert review.id == 1
    assert review.tour is tour
    assert review.user is user


def test_add_review_invalid_rating():
    tour, _, user = make_objects()
    reviews = []
    assert add_review(reviews, tour, user, 10, "Ошибка") is None
    assert reviews == []


def test_get_reviews_for_tour():
    tour, other_tour, user = make_objects()
    reviews = []
    first = add_review(reviews, tour, user, 5, "А")
    add_review(reviews, other_tour, user, 4, "Б")
    assert get_reviews_for_tour(reviews, tour) == [first]


def test_average_rating():
    tour, _, user = make_objects()
    reviews = []
    add_review(reviews, tour, user, 5, "А")
    add_review(reviews, tour, user, 3, "Б")
    assert average_rating(reviews, tour) == 4.0


def test_average_rating_without_reviews():
    tour, _, _ = make_objects()
    assert average_rating([], tour) == 0.0


def test_count_by_status():
    tour, other_tour, user = make_objects()
    reviews = []
    add_review(reviews, tour, user, 5, "А")
    add_review(reviews, tour, user, 3, "Б")
    add_review(reviews, tour, user, 1, "В")
    add_review(reviews, other_tour, user, 5, "Г")
    stats = count_by_status(reviews, tour)
    assert stats["положительных"] == 1
    assert stats["нейтральных"] == 1
    assert stats["отрицательных"] == 1
