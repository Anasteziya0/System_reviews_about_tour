from typing import List, Optional

from models import Review, Tour, User
from models.reviews import (
    add_review,
    average_rating,
    count_by_status,
    get_reviews_for_tour,
    show_reviews,
)
from models.tours import (
    filter_tours_by_price,
    find_tour,
    get_tour_by_id,
    show_tours,
    sort_tours_by_price,
)
from models.users import add_user, find_user, get_user_by_id, show_users
from storage import (
    REVIEWS_FILE,
    TOURS_FILE,
    USERS_FILE,
    load_reviews,
    load_tours,
    load_users,
    save_reviews,
    save_tours,
    save_users,
)
from utils import input_float, input_int, input_text

MENU = (
    "\n Система отзывов об экскурсии \n"
    "1. Показать все экскурсии\n"
    "2. Найти экскурсию по названию\n"
    "3. Отсортировать по цене\n"
    "4. Отобрать по максимальной цене\n"
    "5. Показать отзывы об экскурсии\n"
    "6. Добавить отзыв\n"
    "7. Средний рейтинг экскурсии\n"
    "8. Статистика отзывов\n"
    "9. Показать пользователей\n"
    "10. Найти пользователя\n"
    "11. Добавить пользователя\n"
    "0. Выход"
)


def ask_tour(tours: List[Tour]) -> Optional[Tour]:
    """Запросить ID и найти экскурсию; сообщить, если не найдена."""
    tour = get_tour_by_id(tours, input_int("ID экскурсии: "))
    if tour is None:
        print("Экскурсия с таким ID не найдена.")
    return tour


def ask_user(users: List[User]) -> Optional[User]:
    """Запросить ID и найти пользователя; сообщить, если не найден."""
    user = get_user_by_id(users, input_int("ID пользователя: "))
    if user is None:
        print("Пользователь с таким ID не найден.")
    return user


def create_new_review(
    reviews: List[Review],
    tours: List[Tour],
    users: List[User],
) -> None:
    """Сценарий добавления отзыва: экскурсия, пользователь, оценка."""
    tour = ask_tour(tours)
    if tour is None:
        return
    user = ask_user(users)
    if user is None:
        return
    rating = input_int("Оценка (1–5): ")
    comment = input_text("Комментарий: ")
    review = add_review(reviews, tour, user, rating, comment)
    if review is None:
        print("Ошибка: оценка должна быть от 1 до 5.")
        return
    print(f"Отзыв №{review.id} добавлен. {review.get_status()}.")


def run_menu(
    tours: List[Tour],
    users: List[User],
    reviews: List[Review],
) -> None:
    """Главный цикл меню приложения."""
    while True:
        print(MENU)
        choice = input_int("Выберите пункт: ")

        if choice == 0:
            print("До свидания!")
            break
        elif choice == 1:
            show_tours(tours)
        elif choice == 2:
            query = input("Введите часть названия: ")
            show_tours(find_tour(tours, query))
        elif choice == 3:
            show_tours(sort_tours_by_price(tours))
        elif choice == 4:
            max_price = input_float("Максимальная цена: ")
            show_tours(filter_tours_by_price(tours, max_price))
        elif choice == 5:
            tour = ask_tour(tours)
            if tour:
                show_reviews(get_reviews_for_tour(reviews, tour))
        elif choice == 6:
            create_new_review(reviews, tours, users)
        elif choice == 7:
            tour = ask_tour(tours)
            if tour:
                print(f"Средний рейтинг: {average_rating(reviews, tour):.2f}")
        elif choice == 8:
            tour = ask_tour(tours)
            if tour:
                stats = count_by_status(reviews, tour)
                print(f"Положительных: {stats['положительных']}")
                print(f"Нейтральных: {stats['нейтральных']}")
                print(f"Отрицательных: {stats['отрицательных']}")
        elif choice == 9:
            show_users(users)
        elif choice == 10:
            query = input("Введите имя или email: ")
            show_users(find_user(users, query))
        elif choice == 11:
            name = input_text("Имя: ")
            email = input_text("Email: ")
            add_user(users, name, email)
            print(f"Пользователь добавлен: {users[-1]}")
        else:
            print("Неверный пункт меню.")


def main() -> None:
    """Точка запуска: загрузка данных, меню, сохранение данных."""
    tours = load_tours(TOURS_FILE)
    users = load_users(USERS_FILE)
    reviews = load_reviews(REVIEWS_FILE, tours, users)
    try:
        run_menu(tours, users, reviews)
    except (KeyboardInterrupt, EOFError):
        print("\nЗавершение работы.")
    finally:
        save_tours(TOURS_FILE, tours)
        save_users(USERS_FILE, users)
        save_reviews(REVIEWS_FILE, reviews)


if __name__ == "__main__":
    main()
