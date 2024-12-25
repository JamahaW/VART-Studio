from __future__ import annotations

import math

from figure.abc import Canvas
from figure.impl.transformable import TransformableFigure


class FigureRegistry:
    """
    Реестр фигур, расположенных на холсте.
    Добавить, получить фигуры
    """

    def __init__(self, canvas: Canvas) -> None:
        self.__temp_items_count: int = 0
        self.canvas = canvas
        self.figures = list[TransformableFigure]()

    def add(self, figure: TransformableFigure) -> None:
        """
        Добавить фигуру на холст
        :param figure:
        """
        self.figures.append(figure)
        self.canvas.attachFigure(figure)

    def demoAdd(self) -> None:
        """
        Добавить демо-фигуру
        """
        r = range(0, 271, 1)
        vertices = (
            [math.cos(math.radians(i)) for i in r],
            [math.sin(math.radians(i)) for i in r]
        )

        circle = TransformableFigure(vertices, f"Figure: Test:{self.__temp_items_count}")
        self.__temp_items_count += 1
        self.add(circle)
