"""
Запустить приложение для плоттера
"""
from pathlib import Path

from application.vart import VARTApplication


def _launch():
    _home_path = r"A:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp"
    # _home_path = r"E:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp"
    app = VARTApplication(Path(_home_path))

    app.run("VART-DesktopApp", (1600, 900))


if __name__ == '__main__':
    _launch()
