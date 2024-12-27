from itertools import chain
from math import cos
from math import pi
from math import sin
from pathlib import Path
from typing import Iterable

type Number = int | float

type Vertices[T] = tuple[Iterable[T], Iterable[T]]
type Vec2D[T] = tuple[T, T]


def mix[T: Number](__from: T, __end: T, t: float) -> T:
    return __end * t + (1.0 - t) * __from


class VertexGenerator:

    @classmethod
    def spiral(cls, radius: int, vertex_count: int, k: float = 1.0) -> Vertices[int]:
        k2_pi_p = 2 * k * pi / vertex_count
        r_p = radius / vertex_count

        return (
            map(lambda a: int(sin(a * k2_pi_p) * a * r_p), cls.range(vertex_count)),
            map(lambda a: int(cos(a * k2_pi_p) * a * r_p), cls.range(vertex_count))
        )

    @classmethod
    def circle(cls, radius: int, vertex_count: int) -> Vertices[int]:
        k2_pi_p = 2 * pi / vertex_count

        return (
            map(lambda a: int(sin(a * k2_pi_p) * radius), cls.range(vertex_count)),
            map(lambda a: int(cos(a * k2_pi_p) * radius), cls.range(vertex_count))
        )

    @classmethod
    def rect(cls, width: int, height: int, width_vertex_count: int) -> Vertices[int]:
        half_width = width // 2
        half_height = height // 2

        vertices_on_height = height * width_vertex_count // width

        a = half_width, half_height
        b = -half_width, half_height
        c = -half_width, -half_height
        d = half_width, -half_height

        line_params = (
            (a, b, vertices_on_height),
            (b, c, width_vertex_count),
            (c, d, vertices_on_height),
            (d, a, width_vertex_count)
        )

        x, y = tuple(zip(*(map(lambda _: cls.line(*_), line_params))))
        return chain(*x), chain(*y)

    @classmethod
    def line[T: Number](cls, begin: Vec2D[T], end: Vec2D[T], vertex_count: int) -> Vertices[T]:
        x0, y0 = begin
        x1, y1 = end
        return map(lambda t: mix(x0, x1, t), cls.rangeNorm(vertex_count)), map(lambda t: mix(y0, y1, t), cls.rangeNorm(vertex_count))

    @classmethod
    def rangeNorm(cls, vertex_count: int) -> Iterable[float]:
        return map(lambda n: n / vertex_count, cls.range(vertex_count))

    @staticmethod
    def range(vertex_count: int) -> Iterable[int]:
        return range(vertex_count + 1)

    @classmethod
    def fromImage(cls, path: Path) -> Vertices[int]:
        pass
