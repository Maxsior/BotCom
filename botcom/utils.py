from random import randint
import storage


def generate_uid():
    word = generate_word()
    num = randint(1, 99)
    return f"{word}{num}"


def generate_word():
    while True:
        storage.cursor.execute("SELECT MAX(id) FROM words")
        max_id = storage.cursor.fetchone()[0]
        n = randint(1, max_id)
        storage.cursor.execute("SELECT word FROM words WHERE id = %s", (n,))
        if storage.cursor.rowcount != 0:
            return storage.cursor.fetchone()[0].upper()
