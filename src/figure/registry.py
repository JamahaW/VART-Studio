from __future__ import annotations

import math
from typing import Iterable
from typing import Sequence

from figure.abc import Canvas
from figure.impl.transformable import TransformableFigure
from gen.trajectory import Trajectory


class FigureRegistry:
    """
    Реестр фигур, расположенных на холсте.
    Добавить, получить фигуры
    """

    def __init__(self, canvas: Canvas) -> None:
        self.__temp_items_count: int = 0

        self.canvas = canvas
        self._figures = dict[int, TransformableFigure]()

    def add(self, figure: TransformableFigure) -> None:
        """Добавить фигуру на холст"""
        self._figures[figure.__hash__()] = figure
        self.canvas.addFigure(figure)

    def __onFigureDelete(self, figure: TransformableFigure) -> None:
        self._figures.pop(figure.__hash__())

    def newFigure(self, name: str, vertices: tuple[Sequence[float], Sequence[float]]) -> TransformableFigure:
        return TransformableFigure(vertices, name, self.__onFigureDelete)

    def _makeName(self, source: str) -> str:
        return f"{source.capitalize()}: {self._getCurrentFigureIndex()}"

    def _getCurrentFigureIndex(self) -> int:
        return len(self._figures)

    def addDemoCircle(self) -> None:
        """Добавить демо-фигуру"""
        r = range(0, 271, 1)
        self.add(self.newFigure(self._makeName("test"), (
            [math.cos(math.radians(i)) for i in r],
            [math.sin(math.radians(i)) for i in r]
        )))

    def addDemoTriangle(self) -> None:
        self.add(self.newFigure(self._makeName("triangle"), (
            (0, 0, 1, 0),
            (0, 1, 1, 0)
        )))

    def addDemoRect(self) -> None:
        self.add(self.newFigure(self._makeName("rect"), (
            (-1, -1, 1, 1, -1),
            (-1, 1, 1, -1, -1)
        )))

    def clear(self) -> None:
        for figure in self.getFigures():
            figure.delete()

    def getFigures(self) -> Sequence[TransformableFigure]:
        return list(self._figures.values())

    def getTrajectories(self) -> Iterable[Trajectory]:
        return list(filter(None.__ne__, (figure.toTrajectory() for figure in self.getFigures())))
