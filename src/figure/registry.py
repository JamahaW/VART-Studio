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
        self._figures = list[TransformableFigure]()

    def add(self, figure: TransformableFigure) -> None:
        """Добавить фигуру на холст"""
        self._figures.append(figure)
        self.canvas.attachFigure(figure)

    def addDemoCircle(self) -> None:
        """Добавить демо-фигуру"""
        r = range(0, 271, 1)
        vertices = (
            [math.cos(math.radians(i)) for i in r],
            [math.sin(math.radians(i)) for i in r]
        )

        circle = TransformableFigure(vertices, f"Figure: Test:{self.__temp_items_count}")
        self.__temp_items_count += 1
        self.add(circle)

    def addDemoTriangle(self) -> None:
        triangle = TransformableFigure((
            (0, 0, 0, 0),
            (0, 0, 1, 0)
        ), "triangle")
        self.add(triangle)

    def addDemoRect(self) -> None:
        rect = TransformableFigure((
            (-1, -1, 1, 1, -1),
            (-1, 1, 1, -1, -1)
        ), "rect")
        self.add(rect)

    def getFigures(self) -> Sequence[TransformableFigure]:
        return self._figures

    def getTrajectories(self) -> Iterable[Trajectory]:
        return filter(None.__ne__, (figure.toTrajectory() for figure in self._figures))
