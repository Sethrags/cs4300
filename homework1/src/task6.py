"""Task 6: File handling and word counting."""

from pathlib import Path


def count_words(file_name):
    """Return the number of words in a text file."""
    file_path = Path(file_name)

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    text = file_path.read_text(encoding="utf-8")

    return len(text.split())


if __name__ == "__main__":
    file_path = Path(__file__).parent.parent / "task6_read_me.txt"
    print(count_words(file_path))