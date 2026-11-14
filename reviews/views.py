from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.reviews import get_review_by_id
from storage import (
    REVIEWS_FILE,
    TOURS_FILE,
    USERS_FILE,
    load_reviews,
    load_tours,
    load_users,
)


def reviews(request: HttpRequest) -> HttpResponse:
    """Страница /reviews/: список отзывов из data/reviews.json."""
    tours_list = load_tours(TOURS_FILE)
    users_list = load_users(USERS_FILE)
    reviews_list = load_reviews(REVIEWS_FILE, tours_list, users_list)

    context = {
        "reviews": reviews_list,
    }

    return render(
        request,
        "reviews/review_list.html",
        context,
    )


def review_detail(request: HttpRequest, review_id: int) -> HttpResponse:
    """Страница /reviews/<id>/: информация об отзыве."""
    tours_list = load_tours(TOURS_FILE)
    users_list = load_users(USERS_FILE)
    reviews_list = load_reviews(REVIEWS_FILE, tours_list, users_list)

    review = get_review_by_id(
        reviews_list,
        review_id,
    )

    context = {
        "review": review,
    }

    return render(
        request,
        "reviews/review_detail.html",
        context,
        status=404 if review is None else 200,
    )
