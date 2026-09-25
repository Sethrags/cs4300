from src.task5 import first_three_books, student_database


def test_first_three_books():
    books = first_three_books()

    titles = [book["title"] for book in books]

    assert titles == ["Harry Potter", "The Hobbit", "Percy Jackson"]
    assert len(books) == 3


def test_student_database():
    assert student_database["Seth"] == "1001"
    assert student_database["Alex"] == "1002"