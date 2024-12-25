from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Final
from typing import Sequence

from dearpygui import dearpygui as dpg

from ui.abc import ItemID
from ui.dpg.impl import Axis
from ui.dpg.impl import LineSeries
from ui.dpg.impl import Plot

type Vec2[T] = tuple[T, T]
Vec2f = Vec2[float]
Vec2i = Vec2[int]


class Figure(LineSeries, ABC):
    """Фигура, изображенная на холсте"""

    def __init__(self, vertices: tuple[Sequence[float], Sequence[float]], label: str, size: Vec2i = (0, 0)) -> None:
        super().__init__(label)
        source_x, source_y = vertices
        self._source_vertices_x: Final[Sequence[float]] = source_x
        self._source_vertices_y: Final[Sequence[float]] = source_y
        self.__size = size

    @abstractmethod
    def getTransformedVertices(self) -> tuple[Sequence[float], Sequence[float]]:
        """Получить трансформированные вершины"""

    @abstractmethod
    def attachIntoCanvas(self, canvas: Canvas) -> None:
        """Добавить на холст эту фигуру"""

    def getSize(self) -> Vec2f:
        """Получить масштаб фигуры"""
        return self.__size

    def setSize(self, size: Vec2f) -> None:
        """Установить масштаб фигуры"""
        self.__size = size

    def update(self) -> None:
        """Обновить показания на холста"""
        self.setValue(self.getTransformedVertices())


class Canvas(Plot):

    def __init__(self) -> None:
        super().__init__()
        self.axis = Axis(dpg.mvXAxis)

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self.add(self.axis)

    def addFigure(self, figure: Figure) -> None:
        """Добавить фигуру"""
        figure.attachIntoCanvas(self)
