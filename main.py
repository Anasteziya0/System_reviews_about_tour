from datetime import date



tour_name = "Обзорная экскурсия по историческому центру"
tour_place = "Исторический центр города"
tour_price_str = "2200"
tour_price = int(tour_price_str)

#Просмотр информации об экскурсии
def search_tour(name, place, price):
    print("Название экскурсии:", name)
    print("Места посещения:", place)
    print("Цена за экскурсию:", price)



def rating_status(rating):
    if rating >= 4:
        return "Оценка положительная"
    elif rating == 3:
        return "Оценка нейтральная"
    else:
        return "Оценка отрицательная"


def review(rating, author, comment):
    review_date = date.today()
    return f'{author} поставил(а) оценку: {rating}({rating_status(rating)}) и оставил(а) отзыв: {comment} ({review_date})'


search_tour(tour_name, tour_place, tour_price)
print(review(5, "Анна", "Очень понравилась экскурсия!"))





