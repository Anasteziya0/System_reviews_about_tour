from datetime import date

from storage import save_json

REVIEWS_FILE = "data/reviews.json"


def check_rating(rating: int) -> str:
    """Вернуть текстовый статус оценки."""
    if rating < 1 or rating > 5:
        return "Ошибка: оценка должна быть от 1 до 5"
    if rating >= 4:
        return "Оценка положительная"
    if rating == 3:
        return "Оценка нейтральная"
    return "Оценка отрицательная"


def add_review(
    reviews: list[dict],
    tour_id: int,
    author: str,
    rating: int,
    comment: str,
) -> dict | None:
    if rating < 1 or rating > 5:
        print("Ошибка: оценка должна быть от 1 до 5")
        return None
    review = {
        "tour_id": tour_id,
        "author": author,
        "rating": rating,
        "comment": comment,
        "date": date.today().isoformat(),
    }
    reviews.append(review)
    save_json(REVIEWS_FILE, reviews)
    return review


def get_reviews_for_tour(reviews: list[dict], tour_id: int) -> list[dict]:
    return [review for review in reviews if review["tour_id"] == tour_id]


def average_rating(reviews: list[dict], tour_id: int) -> float:
    tour_reviews = get_reviews_for_tour(reviews, tour_id)
    if not tour_reviews:
        return 0.0
    return sum(review["rating"] for review in tour_reviews) / len(tour_reviews)


def count_by_status(reviews: list[dict], tour_id: int) -> dict:
    stats = {"положительных": 0, "нейтральных": 0, "отрицательных": 0}
    for review in get_reviews_for_tour(reviews, tour_id):
        rating = review["rating"]
        if rating >= 4:
            stats["положительных"] += 1
        elif rating == 3:
            stats["нейтральных"] += 1
        else:
            stats["отрицательных"] += 1
    return stats