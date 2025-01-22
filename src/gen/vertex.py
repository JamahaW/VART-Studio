from itertools import chain
from itertools import pairwise
from math import cos
from math import pi
from math import radians
from math import sin
from pathlib import Path
from typing import Final
from typing import Iterable

Vertices = tuple[Iterable[float], Iterable[float]]

type Number = int | float
type Vec2D[T] = tuple[T, T]
Vec2f = Vec2D[float]
Vec2i = Vec2D[int]


class VertexGenerator:
    MIN_RESOLUTION: Final[int] = 1
    MAX_RESOLUTION: Final[int] = 1000

    MIN_POLYGON_VERTEX_COUNT: Final[int] = 3
    MAX_POLYGON_VERTEX_COUNT: Final[int] = 20

    MIN_SPIRAL_REPEATS: Final[int] = 1
    MAX_SPIRAL_REPEATS: Final[int] = 50

    @classmethod
    def getSpiralRepeatsRange(cls) -> tuple[int, int]:
        return cls.MIN_SPIRAL_REPEATS, cls.MAX_SPIRAL_REPEATS

    @classmethod
    def getResolutionRange(cls) -> tuple[int, int]:
        return cls.MIN_RESOLUTION, cls.MAX_RESOLUTION

    @classmethod
    def getPolygonRange(cls) -> tuple[int, int]:
        return cls.MIN_POLYGON_VERTEX_COUNT, cls.MAX_POLYGON_VERTEX_COUNT

    @classmethod
    def spiral(cls, resolution: int, k: float = 1.0) -> Vertices:
        k2_pi_p = 2 * k * pi / resolution
        return (
            map(lambda a: sin(a * k2_pi_p) * a / resolution, cls.range(resolution)),
            map(lambda a: cos(a * k2_pi_p) * a / resolution, cls.range(resolution))
        )

    @classmethod
    def circle(cls, resolution: int) -> Vertices:
        k2_pi_p = 2 * pi / resolution
        return (
            map(lambda a: sin(a * k2_pi_p), cls.range(resolution)),
            map(lambda a: cos(a * k2_pi_p), cls.range(resolution))
        )

    @classmethod
    def nGon(cls, vertex_count: int, resolution: int) -> Vertices:
        angle = 360 // vertex_count
        angles = tuple(map(radians, range(0, 360, angle)))
        return cls.polygon((map(sin, angles), map(cos, angles)), resolution)

    @classmethod
    def rect(cls, resolution: int) -> Vertices:
        return cls.polygon(((1, -1, -1, 1), (1, 1, -1, -1)), resolution)

    @classmethod
    def polygon(cls, vertices: Vertices, resolution: int) -> Vertices:
        x, y = zip(*(map(lambda _: cls.line(*_), (
            (*pos, resolution)
            for pos in pairwise(cls.appendFirst(zip(*vertices)))
        ))))
        return chain(*x), chain(*y)

    @classmethod
    def line[T: Number](cls, begin: Vec2D[T], end: Vec2D[T], resolution: int) -> Vertices:
        x0, y0 = begin
        x1, y1 = end
        return (
            map(lambda t: cls.mix(x0, x1, t), cls.rangeNorm(resolution)),
            map(lambda t: cls.mix(y0, y1, t), cls.rangeNorm(resolution))
        )

    @classmethod
    def rangeNorm(cls, resolution: int) -> Iterable[float]:
        return map(lambda n: n / resolution, cls.range(resolution))

    @staticmethod
    def range(resolution: int) -> Iterable[int]:
        return range(resolution + 1)

    @staticmethod
    def appendFirst[T](i: Iterable[T]) -> Iterable[T]:
        i = iter(i)
        first = next(i, None)

        if first is not None:
            yield first

        yield from i
        yield first

    @staticmethod
    def mix[T: Number](__from: T, __end: T, t: float) -> T:
        return __end * t + (1.0 - t) * __from

    @classmethod
    def fromImage(cls, path: Path) -> Vertices:
        pass
