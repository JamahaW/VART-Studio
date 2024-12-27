"""Трансформируемая фигура"""

from __future__ import annotations

import math
from typing import Callable
from typing import Optional
from typing import Sequence

from figure.abc import Canvas
from figure.abc import Figure
from figure.abc import Vec2f
from gen.settings import GeneratorSettings
from gen.trajectory import Trajectory
from ui.abc import ItemID
from ui.dpg.impl import Button
from ui.dpg.impl import Checkbox
from ui.dpg.impl import CollapsingHeader
from ui.dpg.impl import DragPoint
from ui.dpg.impl import InputInt
from ui.dpg.impl import Separator
from ui.dpg.impl import SliderInt
from ui.dpg.impl import Text


class TransformableFigure(Figure):

    def __init__(self, vertices: tuple[Sequence[float], Sequence[float]], label: str, on_delete: Callable[[TransformableFigure], None]) -> None:
        super().__init__(vertices, label, (100, 100))

        self._on_delete = on_delete

        self.__sin_angle: float = 0
        self.__cos_angle: float = 0
        self.setRotation(0)

        self._speed_input = SliderInt("Скорость", value_range=GeneratorSettings.getSpeedRange())
        self._tool_id_input = InputInt("Tool-ID", value_range=(1, Trajectory.MAX_TOOL_ID))

        self._position_point = DragPoint(self.__onPositionPointChanged, label="Position")
        self._size_point = DragPoint(self.__onSizeChanged, label="Размер", default_value=self.getSize())
        self._set_controls_visible_checkbox = Checkbox(self.__onSetControlsVisibleChanged, label="Видимость элементов управления", default_value=True)
        self._set_export_checkbox = Checkbox(label="Для печати", default_value=True)

        x, y = self.getSize()
        self._input_scale_x = InputInt("X", self.__updateScaleX, value_range=(0, 10000), default_value=int(x))
        self._input_scale_y = InputInt("Y", self.__updateScaleY, value_range=(0, 10000), default_value=int(y))
        self._input_position_x = InputInt("X", self.__updatePositionX, value_range=(-10000, 10000))
        self._input_position_y = InputInt("Y", self.__updatePositionY, value_range=(-10000, 10000))

    def setRotation(self, angle: int) -> None:
        """Установить поворот"""
        angle = math.radians(angle)
        self.__sin_angle = math.sin(angle)
        self.__cos_angle = math.cos(angle)

    def getPosition(self) -> Vec2f:
        """Получить текущую позицию"""
        return self._position_point.getValue()

    def setPosition(self, position: Vec2f) -> None:
        """Получить позицию фигуры"""
        self._position_point.setValue(position)
        self.__updateSizePoint(*position)

    def setSize(self, size: Vec2f) -> None:
        super().setSize(size)
        size_x, size_y = size
        position_x, position_y = self.getPosition()
        self._size_point.setValue((position_x + size_x, position_y + size_y))

    def toTrajectory(self) -> Optional[Trajectory]:
        """Конвертировать фигуру в траекторию"""

        if not self._set_export_checkbox.getValue():
            return

        x, y = self.getTransformedVertices()
        return Trajectory(
            x_positions=x,
            y_positions=y,
            tool_id=self._tool_id_input.getValue(),
            movement_speed=self._speed_input.getValue()
        )

    def getTransformedVertices(self) -> tuple[Sequence[int], Sequence[int]]:
        transformed_x = list[int]()
        transformed_y = list[int]()

        size_x, size_y = self.getSize()
        position_x, position_y = self.getPosition()

        sin_angle = self.__sin_angle
        cos_angle = self.__cos_angle

        for x, y in zip(self._source_vertices_x, self._source_vertices_y):
            x *= size_x
            y *= size_y

            transformed_x.append(int(cos_angle * x - sin_angle * y + position_x))
            transformed_y.append(int(sin_angle * x + cos_angle * y + position_y))

        return transformed_x, transformed_y

    def attachIntoCanvas(self, canvas: Canvas) -> None:
        canvas.axis.add(self)
        canvas.add(self._position_point)
        canvas.add(self._size_point)
        self.update()

    def delete(self) -> None:
        super().delete()
        self._on_delete(self)
        self._position_point.delete()
        self._size_point.delete()

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)

        (
            CollapsingHeader("Параметры Печати", default_open=True).place(self)
            .add(self._set_export_checkbox)
            .add(self._tool_id_input)
            .add(self._speed_input)
            .add(Separator())
        )

        (
            CollapsingHeader("Трансформация", default_open=True).place(self)
            .add(Text("Масштаб"))
            .add(self._input_scale_x)
            .add(self._input_scale_y)
            .add(Separator())
            .add(InputInt("Поворот", self.__onRotationChanged, value_range=(-360, 360), default_value=0, step_fast=15))
            .add(Separator())
            .add(Text("Позиция"))
            .add(self._input_position_x)
            .add(self._input_position_y)
            .add(Separator())
        )

        self.add(self._set_controls_visible_checkbox)
        self.add(Button("Удалить фигуру", self.delete))

    def __updatePositionX(self, new_x: float) -> None:
        _, y = self.getPosition()
        self.setPosition((new_x, y))
        self.update()

    def __updatePositionY(self, new_y: float) -> None:
        x, _ = self.getPosition()
        self.setPosition((x, new_y))
        self.update()

    def __updateScaleX(self, new_scale_x: float) -> None:
        _, y = self.getSize()
        self.setSize((new_scale_x, y))
        self.update()

    def __updateScaleY(self, new_scale_y: float) -> None:
        x, _ = self.getSize()
        self.setSize((x, new_scale_y))
        self.update()

    def __onPositionPointChanged(self, new_position: Vec2f) -> None:
        position_x, position_y = new_position
        self.__updateSizePoint(position_x, position_y)
        self._input_position_x.setValue(position_x)
        self._input_position_y.setValue(position_y)
        self.update()

    def __updateSizePoint(self, position_x: float, position_y: float) -> None:
        scale_x, scale_y = self.getSize()
        self._size_point.setValue(((position_x + scale_x), (position_y + scale_y)))

    def __onSizeChanged(self, new_scale: Vec2f) -> None:
        scale_x, scale_y = new_scale
        position_x, position_y = self.getPosition()
        x = scale_x - position_x
        y = scale_y - position_y

        self.setSize((x, y))
        self._input_scale_x.setValue(x)
        self._input_scale_y.setValue(y)
        self.update()

    def __onRotationChanged(self, new_angle: int) -> None:
        self.setRotation(new_angle)
        self.update()

    def __onSetControlsVisibleChanged(self, is_visible: bool) -> None:
        self._position_point.setVisible(is_visible)
        self._size_point.setVisible(is_visible)
