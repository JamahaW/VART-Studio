from abc import abstractmethod
from typing import Callable

from figure.impl.transformable import TransformableFigure
from gen.vertex import VertexGenerator
from gen.vertex import Vertices
from ui.abc import ItemID
from ui.dpg.impl import SliderInt


class GenerativeFigure(TransformableFigure):

    def __init__(self, label: str, on_delete: Callable[[TransformableFigure], None]) -> None:
        super().__init__(self._generateVertices(), label, on_delete)

        self._resolution_input = SliderInt(
            "Resolution",
            value_range=VertexGenerator.getResolutionRange(),
            default_value=VertexGenerator.MIN_RESOLUTION
        )

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self.add(self._resolution_input)

    def getResolution(self) -> int:
        return self._resolution_input.getValue()

    @abstractmethod
    def _generateVertices(self) -> Vertices:
        """Сгенерировать фигуру"""

    def getTransformedVertices(self) -> Vertices:
        self.setVertices(self._generateVertices())
        return super().getTransformedVertices()


class PerfectPolygon(GenerativeFigure):

    def _generateVertices(self) -> Vertices:
        return VertexGenerator.rect(self.getResolution())
