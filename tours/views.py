from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.reviews import average_rating
from models.tours import get_tour_by_id
from storage import (
    REVIEWS_FILE,
    TOURS_FILE,
    USERS_FILE,
    load_reviews,
    load_tours,
    load_users,
)


def tours(request: HttpRequest) -> HttpResponse:
    """Страница /tours/: список экскурсий из data/tours.json."""
    tours_list = load_tours(TOURS_FILE)

    context = {
        "tours": tours_list,
    }

    return render(
        request,
        "tours/tour_list.html",
        context,
    )


def tour_detail(request: HttpRequest, tour_id: int) -> HttpResponse:
    """Страница /tours/<id>/: информация об экскурсии и средний рейтинг."""
    tours_list = load_tours(TOURS_FILE)
    tour = get_tour_by_id(tours_list, tour_id)

    context = {
        "tour": tour,
    }
    if tour is not None:
        users_list = load_users(USERS_FILE)
        reviews_list = load_reviews(REVIEWS_FILE, tours_list, users_list)
        context["rating"] = average_rating(reviews_list, tour)

    return render(
        request,
        "tours/tour_detail.html",
        context,
        status=404 if tour is None else 200,
    )
