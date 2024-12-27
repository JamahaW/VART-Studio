"""
Запустить приложение для плоттера
"""
from pathlib import Path

from dearpygui import dearpygui as dpg

from app.application import Application

if __name__ == '__main__':
    dpg.create_context()
    dpg.create_viewport(title="Cable Plotter App", width=1280, height=720)

    home_path = r"A:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp"
    flash_path = r"E:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp"

    APP_PATH = Path(home_path)

    Application(APP_PATH).build()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
