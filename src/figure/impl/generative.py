from abc import abstractmethod
from typing import Callable

from figure.impl.transformable import TransformableFigure
from gen.vertex import VertexGenerator
from gen.vertex import Vertices
from ui.abc import ItemID
from ui.dpg.impl import InputInt
from ui.dpg.impl import SliderInt


class GenerativeFigure(TransformableFigure):

    def __init__(self, label: str, on_delete: Callable[[TransformableFigure], None]) -> None:
        super().__init__((tuple(), tuple()), label, on_delete)

        self._resolution_input = SliderInt(
            "Resolution",
            value_range=VertexGenerator.getResolutionRange(),
            default_value=VertexGenerator.MIN_RESOLUTION,
            on_change=lambda _: self.update(),
        )

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self.add(self._resolution_input)
        # self.setVertices(self.getTransformedVertices())

    def getResolution(self) -> int:
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


class PerfectPolygon(GenerativeFigure):

    def __init__(self, label: str, on_delete: Callable[[TransformableFigure], None]) -> None:
        super().__init__(label, on_delete)

        self._vertex_count = InputInt("Количество вершин", on_change=lambda _: self.update(), width=TransformableFigure.INPUT_WIDTH, default_value=4, value_range=VertexGenerator.getPolygonRange())

    def _generateVertices(self) -> Vertices:
        return VertexGenerator.nGon(self.getVertexCount(), self.getResolution())

    def getVertexCount(self) -> int:
        return self._vertex_count.getValue()

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self.add(self._vertex_count)
