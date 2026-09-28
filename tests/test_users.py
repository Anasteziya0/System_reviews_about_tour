from models import User
from models.users import add_user, find_user, get_user_by_id


def make_users():
    return [
        User(1, "Анна", "anna@example.com"),
        User(2, "Иван", "ivan@example.com"),
    ]


def test_user_creation():
    user = User(1, "Анна", "anna@example.com")
    assert user.id == 1
    assert user.name == "Анна"
    assert user.email == "anna@example.com"


def test_user_str():
    user = User(1, "Анна", "anna@example.com")
    assert str(user) == "Анна <anna@example.com>"


def test_user_from_data():
    data = {"id": 5, "name": "Пётр", "email": "petr@example.com"}
    user = User.from_data(data)
    assert isinstance(user, User)
    assert user.id == 5
    assert user.name == "Пётр"
    assert user.email == "petr@example.com"


def test_add_user():
    users = make_users()
    add_user(users, "Пётр", "petr@example.com")
    assert len(users) == 3
    assert users[-1].id == 3
    assert users[-1].name == "Пётр"


def test_find_user_by_name_and_email():
    users = make_users()
    assert find_user(users, "анна") == [users[0]]
    assert find_user(users, "IVAN@") == [users[1]]
    assert find_user(users, "нет такого") == []


def test_get_user_by_id():
    users = make_users()
    assert get_user_by_id(users, 1) is users[0]
    assert get_user_by_id(users, 99) is None
