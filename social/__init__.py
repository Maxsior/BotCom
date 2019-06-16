import os
import importlib

__exclude_list = ['template', '__pychache__']

modules = {}
for f in os.scandir('social'):
    if f.is_dir() and f.name not in __exclude_list:
        modules[f.name] = importlib.import_module('social.' + f.name)
