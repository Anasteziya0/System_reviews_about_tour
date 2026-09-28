import json
import os
from typing import List

from models import Review, Tour, User
from models.tours import get_tour_by_id
from models.users import get_user_by_id

TOURS_FILE = "data/tours.json"
USERS_FILE = "data/users.json"
REVIEWS_FILE = "data/reviews.json"


def load_json(filename: str) -> List[dict]:
    """Загрузить список словарей из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return []
    except json.JSONDecodeError:
        backup = filename + ".bak"
        os.replace(filename, backup)
        print(
            f"Файл {filename} повреждён, данные не загружены. "
            f"Копия сохранена как {backup}."
        )
        return []


def save_json(filename: str, data: List[dict]) -> None:
    """Сохранить список словарей в JSON-файл."""
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_tours(filename: str) -> List[Tour]:
    """Загрузить экскурсии из JSON и преобразовать их в объекты Tour."""
    tours = []
    for data in load_json(filename):
        try:
            tours.append(
                Tour(
                    tour_id=data["id"],
                    name=data["name"],
                    place=data["place"],
                    price=data["price"],
                    duration=data["duration"],
                )
            )
        except KeyError:
            print(f"Некорректная запись экскурсии пропущена: {data}")
    return tours


def save_tours(filename: str, tours: List[Tour]) -> None:
    """Преобразовать объекты Tour в словари и сохранить в JSON."""
    save_json(filename, [
        {
            "id": tour.id,
            "name": tour.name,
            "place": tour.place,
            "price": tour.price,
            "duration": tour.duration,
        }
        for tour in tours
    ])


def load_users(filename: str) -> List[User]:
    """Загрузить пользователей из JSON и преобразовать в объекты User."""
    users = []
    for data in load_json(filename):
        try:
            users.append(User.from_data(data))
        except KeyError:
            print(f"Некорректная запись пользователя пропущена: {data}")
    return users


def save_users(filename: str, users: List[User]) -> None:
    """Преобразовать объекты User в словари и сохранить в JSON."""
    save_json(filename, [
        {"id": user.id, "name": user.name, "email": user.email}
        for user in users
    ])


def load_reviews(
    filename: str,
    tours: List[Tour],
    users: List[User],
) -> List[Review]:
    """Загрузить отзывы из JSON и восстановить связи с Tour и User."""
    reviews = []
    for data in load_json(filename):
        try:
            tour = get_tour_by_id(tours, data["tour_id"])
            user = get_user_by_id(users, data["user_id"])
            if tour is None or user is None:
                print(
                    f"Отзыв {data['id']} пропущен: "
                    "экскурсия или пользователь не найдены."
                )
                continue
            reviews.append(
                Review(
                    review_id=data["id"],
                    tour=tour,
                    user=user,
                    rating=data["rating"],
                    comment=data["comment"],
                    review_date=data["review_date"],
                )
            )
        except KeyError:
            print(f"Некорректная запись отзыва пропущена: {data}")
    return reviews


def save_reviews(filename: str, reviews: List[Review]) -> None:
    """Заменить объекты Tour и User их идентификаторами и сохранить."""
    save_json(filename, [
        {
            "id": review.id,
            "tour_id": review.tour.id,
            "user_id": review.user.id,
            "rating": review.rating,
            "comment": review.comment,
            "review_date": review.review_date,
        }
        for review in reviews
    ])
