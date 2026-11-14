from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание приложения и навигация."""
    return render(
        request,
        "homepage/index.html",
    )


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Обработчик 404: собственная страница проекта."""
    return render(
        request,
        "homepage/page_not_found.html",
        status=404,
    )
