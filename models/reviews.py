from datetime import date
from typing import List, Optional

from .tours import Tour
from .users import User

STATUS_KEYS = {
    "Оценка положительная": "положительных",
    "Оценка нейтральная": "нейтральных",
    "Оценка отрицательная": "отрицательных",
}


class Review:
    """Отзыв пользователя об экскурсии."""

    def __init__(
        self,
        review_id: int,
        tour: Tour,
        user: User,
        rating: int,
        comment: str,
        review_date: str,
    ) -> None:
        """Создать объект отзыва, связанный с экскурсией и пользователем."""
        self.id = review_id
        self.tour = tour
        self.user = user
        self.rating = rating
        self.comment = comment
        self.review_date = review_date

    @staticmethod
    def validate_rating(rating: int) -> bool:
        """Проверить, что оценка находится в диапазоне от 1 до 5."""
        return 1 <= rating <= 5

    def get_status(self) -> str:
        """Вернуть текстовый статус отзыва по его оценке."""
        return check_rating(self.rating)

    def __str__(self) -> str:
        """Вернуть строковое представление отзыва."""
        return (
            f"{self.user.name} ({self.review_date}): "
            f"{self.rating}/5 — {self.comment}"
        )


def check_rating(rating: int) -> str:
    """Вернуть текстовый статус оценки (функция из ПР1)."""
    if not Review.validate_rating(rating):
        return "Ошибка: оценка должна быть от 1 до 5"
    if rating >= 4:
        return "Оценка положительная"
    if rating == 3:
        return "Оценка нейтральная"
    return "Оценка отрицательная"


def add_review(
    reviews: List[Review],
    tour: Tour,
    user: User,
    rating: int,
    comment: str,
) -> Optional[Review]:
    """Создать отзыв и добавить в коллекцию; при неверной оценке — None."""
    if not Review.validate_rating(rating):
        return None
    new_id = max((review.id for review in reviews), default=0) + 1
    review = Review(
        new_id, tour, user, rating, comment, date.today().isoformat()
    )
    reviews.append(review)
    return review


def get_reviews_for_tour(
    reviews: List[Review],
    tour: Tour,
) -> List[Review]:
    """Вернуть отзывы об указанной экскурсии."""
    return [review for review in reviews if review.tour.id == tour.id]


def average_rating(reviews: List[Review], tour: Tour) -> float:
    """Рассчитать средний рейтинг экскурсии (0.0, если отзывов нет)."""
    tour_reviews = get_reviews_for_tour(reviews, tour)
    if not tour_reviews:
        return 0.0
    return sum(review.rating for review in tour_reviews) / len(tour_reviews)


def count_by_status(reviews: List[Review], tour: Tour) -> dict:
    """Посчитать положительные, нейтральные и отрицательные отзывы."""
    stats = {"положительных": 0, "нейтральных": 0, "отрицательных": 0}
    for review in get_reviews_for_tour(reviews, tour):
        key = STATUS_KEYS.get(review.get_status())
        if key:
            stats[key] += 1
    return stats


def show_reviews(reviews: List[Review]) -> None:
    """Вывести список отзывов."""
    if not reviews:
        print("Отзывов пока нет.")
        return
    print("\n=== Отзывы ===")
    for review in reviews:
        print(review)
