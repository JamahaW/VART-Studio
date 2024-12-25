from __future__ import annotations

import math
from typing import Optional
from typing import Sequence

from figure.abc import Canvas
from figure.abc import Figure
from gen.trajectory import Trajectory

from ui.abc import ItemID
from ui.dpg.impl import Button
from ui.dpg.impl import Checkbox
from ui.dpg.impl import DragPoint
from ui.dpg.impl import Group
from ui.dpg.impl import InputInt
from ui.dpg.impl import Text


class TransformableFigure(Figure):

    def __init__(self, vertices: tuple[Sequence[float], Sequence[float]], label: str) -> None:
        super().__init__(vertices, label, (100, 100))
        self.__source_vertices_x, self.__source_vertices_y = vertices

        self.__sin_angle: float = 0
        self.__cos_angle: float = 0
        self.setRotation(0)

        self._tool_id: int = 0
        self._movement_speed: int = 0

        self._position_point = DragPoint(self.__onPositionChanged, label="Position")
        self._size_point = DragPoint(self.__onSizeChanged, label="Size", default_value=self.getSize())
        self._set_controls_visible_checkbox = Checkbox(self.__onSetControlsVisibleChanged, label="Controls Visibility", default_value=True)
        self._is_export_checkbox = Checkbox(label="Export", default_value=True)
        self._status_text = FigureStatusText()

    def setRotation(self, angle: int) -> None:
        angle = math.radians(angle)
        self.__sin_angle = math.sin(angle)
        self.__cos_angle = math.cos(angle)

    def getPosition(self) -> tuple[float, float]:
        return self._position_point.getValue()

    def setPosition(self, position: tuple[float, float]) -> None:
        self._position_point.setValue(position)

    def setSize(self, size: tuple[float, float]) -> None:
        super().setSize(size)
        size_x, size_y = size
        position_x, position_y = self.getPosition()
        self._size_point.setValue((position_x + size_x, position_y + size_y))

    def toTrajectory(self) -> Optional[Trajectory]:
        if self._is_export_checkbox.getValue():
            return

        x, y = self.getTransformedVertices()
        return Trajectory(
            x_positions=x,
            y_positions=y,
            tool_id=self._tool_id,
            movement_speed=self._movement_speed
        )

    def getTransformedVertices(self) -> tuple[Sequence[int], Sequence[int]]:
        transformed_x = list[int]()
        transformed_y = list[int]()

        size_x, size_y = self.getSize()
        position_x, position_y = self.getPosition()

        sin_angle = self.__sin_angle
        cos_angle = self.__cos_angle

        for x, y in zip(self.__source_vertices_x, self.__source_vertices_y):
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
        self._position_point.delete()
        self._size_point.delete()

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self.add(self._status_text)
        self.add(self._is_export_checkbox)
        self.add(InputInt("ToolID", self.__onToolIdChanged, value_range=(0, Trajectory.MAX_TOOL_ID)))
        self.add(InputInt("Speed", self.__onMovementSpeedChanged, value_range=(0, Trajectory.MAX_SPEED)))
        self.add(self._set_controls_visible_checkbox)
        self.add(Button("Remove", self.delete))
        x, y = self.getSize()
        self.add(InputInt("Scale-X", self.__updateScaleX, value_range=(0, 10000), default_value=int(x)))
        self.add(InputInt("Scale-Y", self.__updateScaleY, value_range=(0, 10000), default_value=int(y)))
        self.add(InputInt("Rotation", self.__onRotationChanged, value_range=(0, 360), step=5, default_value=0))

    def __updateScaleX(self, new_scale_x: float) -> None:
        _, y = self.getSize()
        self.setSize((new_scale_x, y))
        self.update()

    def __updateScaleY(self, new_scale_y: float) -> None:
        x, _ = self.getSize()
        self.setSize((x, new_scale_y))
        self.update()

    def __onMovementSpeedChanged(self, new_speed: int) -> None:
        self._movement_speed = new_speed

    def __onToolIdChanged(self, new_tool_id: int) -> None:
        self._tool_id = new_tool_id

    def __onPositionChanged(self, new_position: tuple[float, float]) -> None:
        position_x, position_y = new_position
        scale_x, scale_y = self.getSize()
        self._size_point.setValue((position_x + scale_x, position_y + scale_y))
        self.update()
        self._status_text.update(new_position, self.getSize())

    def __onSizeChanged(self, new_scale: tuple[float, float]) -> None:
        scale_x, scale_y = new_scale
        position_x, position_y = position = self.getPosition()
        self.setSize((scale_x - position_x, scale_y - position_y))
        self.update()
        self._status_text.update(position, new_scale)

    def __onRotationChanged(self, new_rotation) -> None:
        self.setRotation(new_rotation)
        self.update()

    def __onSetControlsVisibleChanged(self, is_visible: bool) -> None:
        self._position_point.setVisible(is_visible)
        self._size_point.setVisible(is_visible)


class FigureStatusText(Text):

    @staticmethod
    def __getString(position: tuple[float, float], size: tuple[float, float]) -> str:
        px, py = position
        sx, sy = size
        return f"Position: {px:.1f}x{py:.1f}, Size: {sx:.1f}x{sy:.1f}"

    def update(self, position: tuple[float, float], size: tuple[float, float]) -> None:
        self.setValue(self.__getString(position, size))

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self.update((0, 0), (0, 0))
