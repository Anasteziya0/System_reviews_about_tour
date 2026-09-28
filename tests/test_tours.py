from tours import (
    add_tour,
    filter_tours_by_price,
    find_tour,
    sort_tours_by_price,
)


def test_add_tour():
    tours = []
    add_tour(tours, "Тестовая экскурсия", "Центр", 1000, 2)
    assert len(tours) == 1
    assert tours[0]["name"] == "Тестовая экскурсия"


def test_find_tour():
    tours = []
    add_tour(tours, "Обзорная экскурсия", "Центр", 2000, 3)
    add_tour(tours, "Ночная экскурсия", "Набережная", 1500, 2)
    result = find_tour(tours, "ночная")
    assert len(result) == 1
    assert result[0]["name"] == "Ночная экскурсия"


def test_filter_tours_by_price():
    tours = [
        {"id": 1, "name": "A", "place": "X", "price": 1000, "duration": 1},
        {"id": 2, "name": "B", "place": "Y", "price": 3000, "duration": 2},
    ]
    result = filter_tours_by_price(tours, 2000)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_sort_tours_by_price():
    tours = [
        {"id": 1, "name": "A", "place": "X", "price": 3000, "duration": 1},
        {"id": 2, "name": "B", "place": "Y", "price": 1000, "duration": 2},
    ]
    sorted_tours = sort_tours_by_price(tours)
    assert sorted_tours[0]["price"] == 1000
    assert sorted_tours[1]["price"] == 3000