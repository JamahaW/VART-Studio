"""Приложение для маркерного плоттера"""

from __future__ import annotations

from pathlib import Path

from dearpygui import dearpygui as dpg

from figure.registry import FigureRegistry
from ui.dpg.impl import Button
from ui.dpg.impl import FileDialog
from ui.dpg.impl import Menu
from figure.abc import Canvas
from figure.impl.workarea import WorkAreaFigure


class Application:
    """Приложение"""

    def __init__(self) -> None:
        self.file_dialog = FileDialog(
            "Select Image file", self.onImageFileSelected,
            (("png", "Image"),),
            r"A:\Program\Python3\CablePlotterApp\res\images"
        )

        self.work_area = WorkAreaFigure("Work Area")
        self.figure_registry = FigureRegistry(Canvas())

    @staticmethod
    def onImageFileSelected(paths: tuple[Path, ...]) -> None:
        """
        Callback при открытии файла
        :param paths:
        """
        print(paths)

    def _testShowFigures(self) -> None:
        print("\n".join(map(str, self.figure_registry.getTrajectories())))

    def build(self) -> None:
        """Построить UI приложения"""
        with dpg.window() as main_window:
            dpg.set_primary_window(main_window, True)

            with dpg.menu_bar():
                Menu("File").place().add(Button("Open", self.file_dialog.show))

                (
                    Menu("dev").place()
                    .add(Button("app circle", self.figure_registry.addDemoCircle))
                    .add(Button("app triangle", self.figure_registry.addDemoTriangle))
                    .add(Button("app rect", self.figure_registry.addDemoRect))
                    .add(Button("show figures", self._testShowFigures))
                )

                dpg.add_separator()

                (
                    Menu("Show").place()
                    .add(Button("show_implot_demo", dpg.show_implot_demo))
                    .add(Button("show_font_manager", dpg.show_font_manager))
                    .add(Button("show_style_editor", dpg.show_style_editor))
                    .add(Button("show_imgui_demo", dpg.show_imgui_demo))
                    .add(Button("show_item_registry", dpg.show_item_registry))
                    .add(Button("show_metrics", dpg.show_metrics))
                    .add(Button("show_debug", dpg.show_debug))
                )

            with dpg.tab_bar() as tabs:
                with dpg.tab(label="Canvas"):
                    self.figure_registry.canvas.place()

                with dpg.tab(label="Foo"):
                    Button("bar", lambda: print(dpg.get_value(tabs))).place()

        self.figure_registry.canvas.addFigure(self.work_area)
        self.figure_registry.addDemoRect()

        self.work_area.setDeadZone(150, 150, 100, 300, -120)
        self.work_area.setSize((1200, 1000))

        self.makeTheme()

    @staticmethod
    def makeTheme():
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 6)
        dpg.bind_theme(global_theme)
