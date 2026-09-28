from reviews import (
    REVIEWS_FILE,
    add_review,
    average_rating,
    count_by_status,
    get_reviews_for_tour,
)
from storage import load_json
from tours import (
    TOURS_FILE,
    filter_tours_by_price,
    find_tour,
    get_tour_by_id,
    sort_tours_by_price,
)
from utils import input_float, input_int


def show_tours(tours: list[dict]) -> None:
    if not tours:
        print("Список экскурсий пуст.")
        return
    print("\n=== Экскурсии ===")
    for tour in tours:
        print(f"[{tour['id']}] {tour['name']}")
        print(f"    Место: {tour['place']}")
        print(f"    Цена: {tour['price']} руб., длительность: {tour['duration']} ч.")


def show_reviews(reviews: list[dict], tour_id: int) -> None:
    tour_reviews = get_reviews_for_tour(reviews, tour_id)
    if not tour_reviews:
        print("Отзывов пока нет.")
        return
    print("\n=== Отзывы ===")
    for review in tour_reviews:
        print(
            f"{review['author']} ({review['date']}): "
            f"{review['rating']}/5 — {review['comment']}"
        )


def main() -> None:
    tours = load_json(TOURS_FILE)
    reviews = load_json(REVIEWS_FILE)

    menu = (
        "\n Система отзывов об экскурсии \n"
        "1. Показать все экскурсии\n"
        "2. Найти экскурсию по названию\n"
        "3. Отсортировать по цене\n"
        "4. Отобрать по максимальной цене\n"
        "5. Показать отзывы об экскурсии\n"
        "6. Добавить отзыв\n"
        "7. Средний рейтинг экскурсии\n"
        "8. Статистика отзывов\n"
        "0. Выход"
    )

    while True:
        print(menu)
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
            tour_id = input_int("ID экскурсии: ")
            if get_tour_by_id(tours, tour_id):
                show_reviews(reviews, tour_id)
            else:
                print("Экскурсия с таким ID не найдена.")
        elif choice == 6:
            tour_id = input_int("ID экскурсии: ")
            if not get_tour_by_id(tours, tour_id):
                print("Экскурсия с таким ID не найдена.")
                continue
            author = input("Ваше имя: ")
            rating = input_int("Оценка (1–5): ")
            comment = input("Комментарий: ")
            if add_review(reviews, tour_id, author, rating, comment):
                print("Отзыв добавлен.")
        elif choice == 7:
            tour_id = input_int("ID экскурсии: ")
            print(f"Средний рейтинг: {average_rating(reviews, tour_id):.2f}")
        elif choice == 8:
            tour_id = input_int("ID экскурсии: ")
            stats = count_by_status(reviews, tour_id)
            print(f"Положительных: {stats['положительных']}")
            print(f"Нейтральных: {stats['нейтральных']}")
            print(f"Отрицательных: {stats['отрицательных']}")
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()