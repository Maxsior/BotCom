from glob import iglob
import os.path as path
from typing import Dict
import ruamel.yaml as yaml

locales: Dict[str, Dict[str, str]] = {}

default = 'en'


def format(loc: str, key: str, **kwargs: str) -> str:
    locale = locales.get(loc, locales[default])
    return locale.get(key, locales[default][key]).format(**kwargs)


def _update_locales():
    global locales
    base = path.dirname(__file__)
    for fname in iglob(path.join(base, '*.yml')):
        with open(fname, 'tr') as f:
            locale = path.splitext(path.basename(fname))[0]
            locales[locale] = yaml.safe_load(f)


_update_locales()
