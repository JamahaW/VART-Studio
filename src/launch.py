"""
Запустить приложение для плоттера
"""
from dearpygui import dearpygui as dpg

from app.application import Application

if __name__ == '__main__':
    dpg.create_context()
    dpg.create_viewport(title="Cable Plotter App", width=1280, height=720)
    Application().build()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
