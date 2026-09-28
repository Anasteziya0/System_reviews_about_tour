from storage import save_json

TOURS_FILE = "data/tours.json"


def add_tour(
    tours: list[dict],
    name: str,
    place: str,
    price: float,
    duration: int,
) -> dict:
    """Добавить экскурсию в список и сохранить его в JSON-файл."""
    new_id = max((tour["id"] for tour in tours), default=0) + 1
    tour = {
        "id": new_id,
        "name": name,
        "place": place,
        "price": price,
        "duration": duration,
    }
    tours.append(tour)
    save_json(TOURS_FILE, tours)
    return tour


def find_tour(tours: list[dict], query: str) -> list[dict]:
    """Найти экскурсии по части названия (без учёта регистра)."""
    query = query.lower()
    return [tour for tour in tours if query in tour["name"].lower()]


def filter_tours_by_price(tours: list[dict], max_price: float) -> list[dict]:
    """Отобрать экскурсии, цена которых не превышает max_price."""
    return [tour for tour in tours if tour["price"] <= max_price]


def sort_tours_by_price(tours: list[dict]) -> list[dict]:
    """Вернуть экскурсии, отсортированные по возрастанию цены."""
    return sorted(tours, key=lambda tour: tour["price"])


def get_tour_by_id(tours: list[dict], tour_id: int) -> dict | None:
    """Найти экскурсию по идентификатору или вернуть None."""
    for tour in tours:
        if tour["id"] == tour_id:
            return tour
    return None
