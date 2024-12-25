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


class Figure(LineSeries, ABC):

    def __init__(self, vertices: tuple[Sequence[float], Sequence[float]], label: str, size: tuple[int, int] = (0, 0)) -> None:
        super().__init__(label)
        source_x, source_y = vertices
        self.source_vertices_x: Final[Sequence[float]] = source_x
        self.source_vertices_y: Final[Sequence[float]] = source_y
        self.__size = size

    @abstractmethod
    def getTransformedVertices(self) -> tuple[Sequence[float], Sequence[float]]:
        """Получить трансформированные вершины"""

    @abstractmethod
    def attachIntoCanvas(self, canvas: Canvas) -> None:
        """Добавить на холст эту фигуру"""

    def getSize(self) -> tuple[float, float]:
        return self.__size

    def setSize(self, size: tuple[float, float]) -> None:
        self.__size = size

    def update(self) -> None:
        self.setValue(self.getTransformedVertices())


class Canvas(Plot):

    def __init__(self) -> None:
        super().__init__()
        self.axis = Axis(dpg.mvXAxis)

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self.add(self.axis)

    def attachFigure(self, figure: Figure) -> None:
        figure.attachIntoCanvas(self)
