from models import Tour
from models.tours import (
    add_tour,
    filter_tours_by_price,
    find_tour,
    get_tour_by_id,
    sort_tours_by_price,
)


def make_tours():
    return [
        Tour(1, "Обзорная экскурсия", "Центр", 3000, 3),
        Tour(2, "Ночная экскурсия", "Набережная", 1000, 2),
    ]


def test_tour_creation():
    tour = Tour(1, "Обзорная экскурсия", "Центр", 2000, 3)
    assert tour.id == 1
    assert tour.name == "Обзорная экскурсия"
    assert tour.place == "Центр"
    assert tour.price == 2000
    assert tour.duration == 3


def test_tour_str():
    tour = Tour(1, "Обзорная экскурсия", "Центр", 2000, 3)
    assert str(tour) == "Обзорная экскурсия (Центр), 2000 руб., 3 ч."


def test_tour_is_within_budget():
    tour = Tour(1, "Обзорная экскурсия", "Центр", 2000, 3)
    assert tour.is_within_budget(2500)
    assert tour.is_within_budget(2000)
    assert not tour.is_within_budget(1500)


def test_add_tour():
    tours = []
    tour = add_tour(tours, "Тестовая экскурсия", "Центр", 1000, 2)
    assert isinstance(tour, Tour)
    assert tours == [tour]
    assert tour.id == 1
    assert add_tour(tours, "Вторая", "Парк", 500, 1).id == 2


def test_find_tour():
    result = find_tour(make_tours(), "ночная")
    assert len(result) == 1
    assert result[0].name == "Ночная экскурсия"


def test_filter_tours_by_price():
    result = filter_tours_by_price(make_tours(), 2000)
    assert [tour.id for tour in result] == [2]


def test_sort_tours_by_price():
    result = sort_tours_by_price(make_tours())
    assert [tour.price for tour in result] == [1000, 3000]


def test_get_tour_by_id():
    tours = make_tours()
    assert get_tour_by_id(tours, 2) is tours[1]
    assert get_tour_by_id(tours, 99) is None
