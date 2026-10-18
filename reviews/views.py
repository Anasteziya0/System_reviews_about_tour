from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page, rating_badge
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

    items = ""
    for review in reviews_list:
        badge = rating_badge(review.rating)
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/reviews/{review.id}/">
                {escape(review.tour.name)} – {review.review_date}
            </a>
            <span class="badge {badge}">
                {review.rating} / 5
            </span>
        </li>
        """
    content = f"""
    <h1>Отзывы</h1>
    <ul class="list-group">
        {items}
    </ul>
    """
    return HttpResponse(
        page("Система отзывов – отзывы", content)
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
    if review is None:
        content = """
        <h1 class="text-danger">
            Отзыв не найден
        </h1>
        <a href="/reviews/"
           class="btn btn-outline-secondary">
            ← к списку отзывов
        </a>
        """
        return HttpResponse(
            page("Отзыв не найден", content),
            status=404,
        )

    status = review.get_status()
    badge = rating_badge(review.rating)
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                Отзыв №{review.id}
            </h5>
            <p class="card-text">
                Экскурсия: {escape(review.tour.name)}
            </p>
            <p class="card-text">
                Автор: {escape(review.user.name)}
            </p>
            <p class="card-text">
                Дата: {review.review_date}
            </p>
            <p class="card-text">
                Оценка: {review.rating} из 5
                <span class="badge {badge}">
                    {status}
                </span>
            </p>
            <p class="card-text">
                Комментарий: {escape(review.comment)}
            </p>
            <a href="/reviews/"
               class="btn btn-outline-secondary">
                ← к списку отзывов
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(
            f"Отзыв №{review.id}",
            content,
        ),
        status=200,
    )
