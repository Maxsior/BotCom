import os
import importlib

__exclude_list = ['template', '__pycache__']

modules = {}
for f in os.scandir(os.path.join(os.path.dirname(__file__))):
    if f.is_dir() and f.name not in __exclude_list:
        modules[f.name] = importlib.import_module('messengers.' + f.name)
