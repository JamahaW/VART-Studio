from abc import abstractmethod
from typing import Callable

from figure.impl.transformable import TransformableFigure
from gen.vertex import VertexGenerator
from gen.vertex import Vertices
from ui.widgets.abc import ItemID
from ui.widgets.dpg.impl import CollapsingHeader
from ui.widgets.dpg.impl import InputInt
from ui.widgets.dpg.impl import SliderInt


class GenerativeFigure(TransformableFigure):

    def __init__(self, label: str, on_delete: Callable[[TransformableFigure], None]) -> None:
        super().__init__((tuple(), tuple()), label, on_delete)

        self._resolution_input = SliderInt(
            "Разрешение",
            value_range=VertexGenerator.getResolutionRange(),
            default_value=VertexGenerator.MIN_RESOLUTION,
            on_change=lambda _: self.update(),
        )

        self._header = CollapsingHeader("Прочее", default_open=True)

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self._header.place(self).add(self._resolution_input)

    def getResolution(self) -> int:
        """Получить разрешение"""
        return self._resolution_input.getValue()

    @abstractmethod
    def _generateVertices(self) -> Vertices:
        """Сгенерировать фигуру"""

    def getTransformedVertices(self) -> Vertices:
        self.setVertices(self._generateVertices())
        return super().getTransformedVertices()


class RectFigure(GenerativeFigure):

    def _generateVertices(self) -> Vertices:
        return VertexGenerator.rect(self.getResolution())


class CircleFigure(GenerativeFigure):

    def _generateVertices(self) -> Vertices:
        return VertexGenerator.circle(self.getResolution())


class SpiralFigure(GenerativeFigure):

    def __init__(self, label: str, on_delete: Callable[[TransformableFigure], None]) -> None:
        super().__init__(label, on_delete)
        self._repeats_count = InputInt("Кол-во витков", on_change=lambda _: self.update(), width=TransformableFigure.INPUT_WIDTH, default_value=1, value_range=VertexGenerator.getSpiralRepeatsRange())

    def _generateVertices(self) -> Vertices:
        return VertexGenerator.spiral(self.getResolution(), self._repeats_count.getValue())

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self._header.add(self._repeats_count)


class PolygonFigure(GenerativeFigure):

    def __init__(self, label: str, on_delete: Callable[[TransformableFigure], None]) -> None:
        super().__init__(label, on_delete)
        self._vertex_count = InputInt("Вершины", on_change=lambda _: self.update(), width=TransformableFigure.INPUT_WIDTH, default_value=6, value_range=VertexGenerator.getPolygonRange())

    def _generateVertices(self) -> Vertices:
        return VertexGenerator.nGon(self.getVertexCount(), self.getResolution())

    def getVertexCount(self) -> int:
        """Получить количество вершин полигона"""
        return self._vertex_count.getValue()

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self._header.add(self._vertex_count)
