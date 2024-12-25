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

    def __init__(self) -> None:
        self.logger = LoggerWidget()
        self.image_file_dialog = FileDialog(
            "Select Image file", self.onImageFileSelected,
            (("png", "Image"),),
            r"A:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp\res\images"
        )

        self.export_file_dialog = FileDialog(
            "Select Dest Export Bytecode", lambda paths: self._onWriteBytecode(paths[0]),
            extensions=(("blc", "VART ByteLang ByteCode"),),
            default_path=r"A:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp\res\out"
        )

        self.work_area = WorkAreaFigure("Work Area")
        self.figure_registry = FigureRegistry(Canvas())

        self.generator_settings = GeneratorSettings(
            speed=5,
            end_speed=10,
            tool_none=0,
            disconnect_distance_mm=5,
            tool_change_duration_ms=500
        )
        self.bytecode_writer = CodeWriter.simpleSetup(r"A:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp\res")

    @staticmethod
    def onImageFileSelected(paths: Sequence[Path]) -> None:
        """
        Callback при открытии файла
        :param paths:
        """
        print(paths)

    def _testShowFigures(self) -> None:
        print("\n".join(map(str, self.figure_registry.getTrajectories())))

    def _onWriteBytecode(self, output_path: Path) -> None:
        with open(output_path, "wb") as bytecode_stream:
            result = self.bytecode_writer.run(self.generator_settings, self.figure_registry.getTrajectories(), bytecode_stream, LogFlag.PROGRAM_SIZE | LogFlag.COMPILATION_TIME | LogFlag.BYTECODE)
            self.logger.write(result.getMessage())

    def build(self) -> None:
        """Построить UI приложения"""
        with dpg.window() as main_window:
            dpg.set_primary_window(main_window, True)

            with dpg.menu_bar():
                (
                    Menu("File").place()
                    .add(Button("Open", self.image_file_dialog.show))
                    .add(Button("Export", self.export_file_dialog.show))
                )

                (
                    Menu("dev").place()
                    .add(Button("circle", self.figure_registry.addDemoCircle))
                    .add(Button("triangle", self.figure_registry.addDemoTriangle))
                    .add(Button("rect", self.figure_registry.addDemoRect))
                    .add(Button("print trajectories", self._testShowFigures))
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
                with dpg.tab(label="Canvas View"):
                    self.figure_registry.canvas.place()

                with dpg.tab(label="Setting"):
                    CodeGeneratorSettngsWidget(self.generator_settings).place()

                with dpg.tab(label="Logs"):
                    self.logger.place()

        self.figure_registry.canvas.addFigure(self.work_area)
        self.figure_registry.addDemoRect()

        self.work_area.setDeadZone(150, 150, 100, 300, -120)
        self.work_area.setSize((1200, 1200))

        self._makeTheme()

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
