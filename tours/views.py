from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page, rating_badge
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
    items = ""
    for tour in load_tours(TOURS_FILE):
        text = f"{escape(tour.name)} – {escape(tour.place)}, {tour.price} руб."
        items += (
            '<li class="list-group-item">'
            f'<a href="/tours/{tour.id}/">{text}</a>'
            "</li>"
        )
    content = f"""
    <h1>Экскурсии</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Система отзывов – экскурсии", content))


def tour_detail(request: HttpRequest, tour_id: int) -> HttpResponse:
    """Страница /tours/<id>/: информация об экскурсии и средний рейтинг."""
    tours_list = load_tours(TOURS_FILE)

    tour = get_tour_by_id(tours_list, tour_id)

    if tour is None:
        content = """
        <h1 class="text-danger">Экскурсия не найдена</h1>
        <a href="/tours/" class="btn btn-outline-secondary">
            ← к списку экскурсий
        </a>
        """
        return HttpResponse(
            page("Экскурсия не найдена", content),
            status=404,
        )
    users_list = load_users(USERS_FILE)
    reviews_list = load_reviews(REVIEWS_FILE, tours_list, users_list)
    rating = average_rating(reviews_list, tour)
    if rating:
        rating_text = f"{rating:.1f} из 5"
        badge = rating_badge(rating)
    else:
        rating_text = "отзывов пока нет"
        badge = "bg-secondary"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(tour.name)}</h5>

            <p class="card-text">
                <strong>ID:</strong> {tour.id}
            </p>

            <p class="card-text">
                <strong>Место:</strong> {escape(tour.place)}
            </p>

            <p class="card-text">
                <strong>Цена:</strong> {tour.price} руб.
            </p>

            <p class="card-text">
                <strong>Длительность:</strong> {tour.duration} ч.
            </p>

            <p class="card-text">
                Средний рейтинг:
                <span class="badge {badge}">
                    {rating_text}
                </span>
            </p>

            <a href="/tours/"
               class="btn btn-outline-secondary">
                ← к списку экскурсий
            </a>
        </div>
    </div>
    """

    return HttpResponse(
        page(tour.name, content),
        status=200,
    )
