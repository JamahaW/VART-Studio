"""
Запустить приложение для плоттера
"""
from pathlib import Path

from application.vart import VARTApplication


def _launch():
    # _home_path = r"A:\Projects\VART\Code\VART-DesktopApp"
    _home_path = r"E:\Projects\VART\Code\VART-DesktopApp"
    app = VARTApplication(Path(_home_path))

    app.run("VART-Studio", (1280, 720))


if __name__ == '__main__':
    _launch()
