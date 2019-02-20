import json
from urllib.request import urlopen
from random import randint
import storage

def generate_uid():
    word = generate_word()
    num = randint(1, 100)
    return f"{word}{str(num)}"

def normalize(text):
    # TODO нужна ли нормализация?
    return text

def generate_word():
    storage._init()
    while True:
        n = randint(1, 55)
        storage.cursor.execute(f"SELECT word FROM words WHERE id = {n}")
        if storage.cursor.rowcount != 0:
            return storage.cursor.fetchone()[0].upper()



