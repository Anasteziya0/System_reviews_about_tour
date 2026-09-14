from datetime import date


excursion_name = "Обзорная экскурсия по Москве"
excursion_date = date(2026, 9, 20)
excursion_place = "Красная площадь"
excursion_price = 1500


def show_excursion_info(name, place, price):
    print("Информация об экскурсии")
    print(f"Название: {name}")
    print(f"Место проведения: {place}")
    print(f"Стоимость: {price} руб.")


def check_rating(rating):
    if rating < 1 or rating > 5:
        return "Ошибка: оценка должна быть от 1 до 5"
    return "Оценка верна"


def get_review_status(rating):

    if rating >= 4:
        return "Положительный отзыв"
    elif rating == 3:
        return "Нейтральный отзыв"
    else:
        return "Отрицательный отзыв"


show_excursion_info(excursion_name, excursion_place, excursion_price)

user_rating = int(input("\nПоставьте оценку экскурсии (1–5): "))

print(check_rating(user_rating))

if 1 <= user_rating <= 5:
    print(get_review_status(user_rating))