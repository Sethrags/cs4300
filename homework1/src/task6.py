from pathlib import Path


def count_words(file_name):
    file_path = Path(file_name)

    text = file_path.read_text()

    return len(text.split())


if __name__ == "__main__":
    file_path = Path(__file__).parent.parent / "task6_read_me.txt"
    print(count_words(file_path))