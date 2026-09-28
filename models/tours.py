from typing import List, Optional


class Tour:
    """Экскурсия, о которой пользователи оставляют отзывы."""

    def __init__(
        self,
        tour_id: int,
        name: str,
        place: str,
        price: float,
        duration: int,
    ) -> None:
        """Создать объект экскурсии."""
        self.id = tour_id
        self.name = name
        self.place = place
        self.price = price
        self.duration = duration

    def is_within_budget(self, max_price: float) -> bool:
        """Проверить, что цена экскурсии не превышает max_price."""
        return self.price <= max_price

    def __str__(self) -> str:
        """Вернуть строковое представление экскурсии."""
        return (
            f"{self.name} ({self.place}), "
            f"{self.price} руб., {self.duration} ч."
        )


def add_tour(
    tours: List[Tour],
    name: str,
    place: str,
    price: float,
    duration: int,
) -> Tour:
    """Создать экскурсию, добавить её в коллекцию и вернуть."""
    new_id = max((tour.id for tour in tours), default=0) + 1
    tour = Tour(new_id, name, place, price, duration)
    tours.append(tour)
    return tour


def find_tour(tours: List[Tour], query: str) -> List[Tour]:
    """Найти экскурсии по части названия (без учёта регистра)."""
    query = query.lower()
    return [tour for tour in tours if query in tour.name.lower()]


def filter_tours_by_price(
    tours: List[Tour],
    max_price: float,
) -> List[Tour]:
    """Отобрать экскурсии, цена которых не превышает max_price."""
    return [tour for tour in tours if tour.is_within_budget(max_price)]


def sort_tours_by_price(tours: List[Tour]) -> List[Tour]:
    """Вернуть экскурсии, отсортированные по возрастанию цены."""
    return sorted(tours, key=lambda tour: tour.price)


def get_tour_by_id(tours: List[Tour], tour_id: int) -> Optional[Tour]:
    """Найти экскурсию по идентификатору или вернуть None."""
    for tour in tours:
        if tour.id == tour_id:
            return tour
    return None


def show_tours(tours: List[Tour]) -> None:
    """Вывести список экскурсий."""
    if not tours:
        print("Экскурсии не найдены.")
        return
    print("\n=== Экскурсии ===")
    for tour in tours:
        print(f"[{tour.id}] {tour}")
