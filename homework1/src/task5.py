favorite_books = [
    {"title": "Harry Potter", "author": "J. K. Rowling"},
    {"title": "The Hobbit", "author": "J. R. R. Tolkien"},
    {"title": "Percy Jackson", "author": "Rick Riordan"},
    {"title": "The Hunger Games", "author": "Suzanne Collins"},
]

student_database = {
    "Seth": "1001",
    "Alex": "1002",
    "Jordan": "1003",
}


def first_three_books():
    return favorite_books[:3]


if __name__ == "__main__":
    for book in first_three_books():
        print(book["title"], "by", book["author"])