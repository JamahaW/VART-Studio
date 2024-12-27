"""Приложение для маркерного плоттера"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from dearpygui import dearpygui as dpg

from app.widgets.settings import CodeGeneratorSettngsWidget
from bytelang.utils import LogFlag
from figure.abc import Canvas
from figure.impl.workarea import WorkAreaFigure
from figure.registry import FigureRegistry
from gen.settings import GeneratorSettings
from gen.writer import CodeWriter
from ui.custom.logger import LoggerWidget
from ui.dpg.impl import Button
from ui.dpg.impl import FileDialog
from ui.dpg.impl import Menu


class Application:
    """Приложение"""

    def __init__(self, resources_path: Path) -> None:
        self._logger = LoggerWidget()
        self._log_flags = LogFlag.PROGRAM_SIZE | LogFlag.COMPILATION_TIME  # | LogFlag.BYTECODE

        self._image_file_dialog = FileDialog(
            "Укажите файл изображения для вставки", self.onImageFileSelected,
            (("png", "Image"),),
            resources_path / "res/images"
        )

        self._export_file_dialog = FileDialog(
            "Укажите файл для экспорта", lambda paths: self._onWriteBytecode(paths[0]),
            extensions=(("blc", "VART ByteCode"),),
            default_path=(resources_path / "res/out")
        )

        self._work_area = WorkAreaFigure("Рабочая область")

        self._figure_registry = FigureRegistry(Canvas())

        self._generator_settings = GeneratorSettings(
            speed=5,
            end_speed=10,
            tool_none=0,
            disconnect_distance_mm=5,
            tool_change_duration_ms=500
        )
        self._bytecode_writer = CodeWriter.simpleSetup(resources_path / "res")

    @staticmethod
    def onImageFileSelected(paths: Sequence[Path]) -> None:
        """
        Callback при открытии файла
        :param paths:
        """
        print(paths)

    def _printTrajectories(self) -> None:
        self._logger.write("\n".join(map(str, self._figure_registry.getTrajectories())))

    def _onWriteBytecode(self, output_path: Path) -> None:
        with open(output_path, "wb") as bytecode_stream:
            trajectories = self._figure_registry.getTrajectories()

            result = self._bytecode_writer.run(
                self._generator_settings,
                trajectories,
                bytecode_stream,
                self._log_flags
            )

            self._logger.write(result.getMessage())

    def build(self) -> None:
        """Построить UI приложения"""
        with dpg.window() as main_window:
            dpg.set_primary_window(main_window, True)

            with dpg.menu_bar():
                (
                    Menu("Файл").place()
                    .add(Button("Открыть", self._image_file_dialog.show))
                    .add(Button("Экспорт", self._export_file_dialog.show))
                )

                dpg.add_separator()

                Button("Очистить", self._figure_registry.clear).place()

                (
                    Menu("Вставка").place()
                    .add(Button("Полигон", self._figure_registry.addPolygon))
                    .add(Button("Прямоугольник", self._figure_registry.addDemoRect))
                )

                dpg.add_separator()

                (
                    Menu("Dev").place()
                    .add(Button("Вывод траекторий", self._printTrajectories))
                    .add(Button("show_implot_demo", dpg.show_implot_demo))
                    .add(Button("show_font_manager", dpg.show_font_manager))
                    .add(Button("show_style_editor", dpg.show_style_editor))
                    .add(Button("show_imgui_demo", dpg.show_imgui_demo))
                    .add(Button("show_item_registry", dpg.show_item_registry))
                    .add(Button("show_metrics", dpg.show_metrics))
                    .add(Button("show_debug", dpg.show_debug))
                )

            with dpg.tab_bar():
                with dpg.tab(label="Область печати"):
                    self._figure_registry.canvas.place()

                with dpg.tab(label="Параметры"):
                    CodeGeneratorSettngsWidget(self._generator_settings).place()

                with dpg.tab(label="Logs"):
                    self._logger.place()

                with dpg.tab(label="Test"):
                    pass

        self._figure_registry.canvas.addFigure(self._work_area)
        self._figure_registry.addPolygon()

        self._work_area.setDeadZone(150, 150, 100, 300, -120)
        self._work_area.setSize((1200, 1200))

        self._makeTheme()

        with dpg.font_registry():
            with dpg.font(r"res/fonts/Roboto-Mono/RobotoMono.ttf", 20, default_font=True) as font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

        dpg.bind_font(font)

    @staticmethod
    def _makeTheme():
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 6)
        dpg.bind_theme(global_theme)
