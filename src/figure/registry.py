from __future__ import annotations

from typing import Iterable
from typing import Sequence

from figure.abc import Canvas
from figure.impl.generative import PolygonFigure
from figure.impl.generative import RectFigure
from figure.impl.transformable import TransformableFigure
from gen.trajectory import Trajectory


class FigureRegistry:
    """Реестр фигур, расположенных на холсте"""

    def __init__(self, canvas: Canvas) -> None:
        self.canvas = canvas
        self._figures = dict[int, TransformableFigure]()

    def add(self, figure: TransformableFigure) -> None:
        """Добавить фигуру на холст"""
        self._figures[figure.__hash__()] = figure
        self.canvas.addFigure(figure)

    def __onFigureDelete(self, figure: TransformableFigure) -> None:
        self._figures.pop(figure.__hash__())

    def _makeName(self, source: str) -> str:
        return f"{source.capitalize()}: {self._getCurrentFigureIndex()}"

    def _getCurrentFigureIndex(self) -> int:
        return len(self._figures)

    def addPolygon(self) -> None:
        """Добавить полигон"""
        self.add(PolygonFigure(self._makeName("Полигон"), self.__onFigureDelete))

    def addDemoRect(self) -> None:
        """Добавить демо-прямоугольник"""
        self.add(RectFigure(self._makeName("Прямоугольник"), self.__onFigureDelete))

    def clear(self) -> None:
        """Удалить все фигуры"""
        for figure in self.getFigures():
            figure.delete()

    def getFigures(self) -> Sequence[TransformableFigure]:
        """Получить все фигуры"""
        return list(self._figures.values())

    def getTrajectories(self) -> Iterable[Trajectory]:
        """Получить все траектории"""
        return list(filter(None.__ne__, (figure.toTrajectory() for figure in self.getFigures())))
