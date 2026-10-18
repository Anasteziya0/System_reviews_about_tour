from django.http import HttpRequest, HttpResponse
from django.utils.html import escape


def page(title: str, content: str) -> str:
    """Собрать HTML-страницу: каркас, Bootstrap, навигация, содержимое."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/tours/">Экскурсии</a>
        <a class="nav-link" href="/reviews/">Отзывы</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def rating_badge(rating: float) -> str:
    """Вернуть класс Bootstrap-бейджа для оценки или среднего рейтинга."""
    if rating >= 4:
        return "bg-success"
    if rating >= 3:
        return "bg-warning text-dark"
    return "bg-danger"


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание приложения и навигация."""
    content = """
    <h1 class="display-4">Отзывы об экскурсиях</h1>
    <p class="lead">Система отзывов об экскурсиях.</p>
    <p>Основные разделы:</p>
    <a href="/tours/" class="btn btn-primary me-2">Экскурсии</a>
    <a href="/reviews/" class="btn btn-secondary">Отзывы</a>
    """
    return HttpResponse(page("Система отзывов об экскурсиях", content))


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Обработчик 404: собственная страница проекта."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
