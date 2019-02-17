import json
from urllib.request import urlopen
from random import randint


def generate_uid():
    res = urlopen("http://free-generator.ru/generator.php?action=word&type=1")
    word = json.loads(res.read().decode())['word']['word'].upper()
    num = randint(1, 100)
    return f"{word}{num}"


def normalize(text):
    # TODO нужна ли нормализация?
    return text
