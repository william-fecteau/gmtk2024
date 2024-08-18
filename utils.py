import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_max_worlds() -> int:
    path = resource_path('res/worlds/')

    return len([file for file in os.listdir(path) if os.path.isdir(path + file)])


def get_max_levels_per_world(world_number: int) -> int:
    path = resource_path(f'res/worlds/{world_number}/')

    return len([file for file in os.listdir(path) if os.path.isfile(path + file)])
