"""Загрузчик OBJ файла"""
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from itertools import chain
from math import cos
from math import hypot
from math import radians
from math import sin
from math import sqrt
from pathlib import Path
from typing import Callable
from typing import ClassVar
from typing import Final
from typing import Iterable
from typing import Optional
from typing import Sequence
from typing import TextIO

from figure.impl.generative import GenerativeFigure
from gen.vertex import Vertices
from ui.widgets.abc import ItemID
from ui.widgets.custom.input2d import InputInt2D
from ui.widgets.dpg.impl import Checkbox
from ui.widgets.dpg.impl import CollapsingHeader
from ui.widgets.dpg.impl import SliderInt


@dataclass(frozen=True)
class Vector3D:
    x: float
    y: float
    z: float

    @classmethod
    def fromParts(cls, parts: Iterable[str]) -> Vector3D:
        return cls(*map(float, parts))

    @classmethod
    def avg(cls, v: Sequence[Vector3D]) -> Vector3D:
        _l = len(v)

        return Vector3D(
            sum(n.x for n in v) / _l,
            sum(n.y for n in v) / _l,
            sum(n.z for n in v) / _l,
        )

    def length(self) -> float:
        return hypot(self.x, self.y, self.z)

    def normalized(self) -> Vector3D:
        _l = self.length()
        return Vector3D(self.x / _l, self.y / _l, self.z / _l)

    def dist(self, v: Vector3D) -> float:
        return hypot(self.x - v.x, self.y - v.y, self.z - v.z)

    def add(self, v: Vector3D) -> Vector3D:
        return Vector3D(self.x + v.x, self.y + v.y, self.z + v.z)

    def rotated_x(self, angle: float) -> Vector3D:
        r = radians(angle)
        c = cos(r)
        s = sin(r)
        return Vector3D(
            self.x,
            self.y * c - self.z * s,
            self.y * s + self.z * c
        )

    def rotated_y(self, angle: float) -> Vector3D:
        r = radians(angle)
        c = cos(r)
        s = sin(r)
        return Vector3D(
            self.x * c + self.z * s,
            self.y,
            -self.x * s + self.z * c
        )

    def dot(self, v: Vector3D) -> float:
        return self.x * v.x + self.y * v.y + self.z * v.z


class Projector(ABC):
    """Проектор"""

    @abstractmethod
    def apply(self, v: Vector3D) -> tuple[float, float]:
        """Спроецировать вектор на дисплей"""


class IsometricProjector(Projector):

    def apply(self, v: Vector3D) -> tuple[float, float]:
        return (
            (v.x - v.z) * cos(radians(30)),
            (v.x + v.z) * sin(radians(30)) + v.y
        )


@dataclass
class PerspectiveProjector(Projector):
    def __init__(self, focal: float = 0.5, epsilon: float = 1e-9):
        self.focal = focal
        self.epsilon = epsilon  # Минимальное значение для избежания деления на 0

    def apply(self, v: Vector3D) -> tuple[float, float]:
        safe_z = v.z if abs(v.z) > self.epsilon else (
            self.epsilon if v.z >= 0 else -self.epsilon
        )

        return (
            self.focal * v.x / safe_z,
            self.focal * v.y / safe_z
        )


@dataclass
class _FaceData:
    # _cameraVertex: ClassVar = Vector3D(-sqrt(2) * sqrt(3) / 4, 0.5, -sqrt(2) * sqrt(3) / 4)
    _cameraVertex: ClassVar = Vector3D(-1, 1, -1)

    vertices: list[Vector3D]
    normal: Vector3D
    centroid: Vector3D

    @classmethod
    def parse(cls, parts: Iterable[str], model: _ModelData, v_offset: int, n_offset: int) -> _FaceData:
        vertices = list()
        normals = list()

        for part in parts:
            v, _, n = part.split('/')

            v_index = int(v) - v_offset
            vertices.append(model.vertices[v_index])

            n_index = int(n) - n_offset
            normals.append(model.normals[n_index])

        return cls(vertices, Vector3D.avg(normals), Vector3D.avg(vertices))

    def isVisible(self, n: Vector3D) -> bool:
        return self._cameraVertex.dot(n) >= 0

    def transform(self, t: Callable[[Vector3D], Vector3D], face_culling: bool) -> Iterable[Vector3D]:
        """
        Трансформация грани
        :param t: трансформация вектора
        :param face_culling:
        :return:
        """
        if face_culling and not self.isVisible(t(self.normal)):
            return ()

        return map(t, self.vertices)


@dataclass
class _ModelData:
    vertices: list[Vector3D]
    normals: list[Vector3D]
    faces: list[_FaceData]

    def sortFaces(self) -> None:
        visible_faces = self.faces

        sorted_faces = [visible_faces[0]]
        used = {0}

        while len(used) < len(visible_faces):
            last_center = sorted_faces[-1].centroid

            # Находим ближайшую неиспользованную грань
            min_dist = float('inf')
            next_idx = 0

            for i, f in enumerate(visible_faces):
                if i not in used:
                    dist = f.centroid.dist(last_center)

                    if dist < min_dist:
                        min_dist = dist
                        next_idx = i

            sorted_faces.append(visible_faces[next_idx])

            used.add(next_idx)

        self.faces = sorted_faces


class ObjFigure(GenerativeFigure):

    def __init__(self, label: str, on_delete: Callable, on_clone: Callable, model: _ModelData) -> None:
        super().__init__(label, on_delete, on_clone)

        self._model = model
        self._isometric_projector = IsometricProjector()
        self._perspective_projector = PerspectiveProjector(0.5)

        update_ = lambda _: self.update()

        def update_focus(f: float):
            self._perspective_projector.focal = f / 100
            self.update()

        self._rotation_XY = InputInt2D(
            "Поворот 2D",
            update_,
            value_range=(-360, 360),
            step_fast=5,
            reset_button=True,
            is_horizontal=True
        )

        self._position_XY = InputInt2D(
            "Смещение XY",
            update_,
            value_range=(-200, 200),
            reset_button=True,
        )

        self._use_perspective = Checkbox(update_, label="Использовать перспективу")
        self._sort_faces = Checkbox(update_, label="Сортировка граней", default_value=False)
        self._culling_k = SliderInt("culling %", update_, value_range=(-100, 100), default_value=50)
        self._face_culling = Checkbox(update_focus, label="Отсечение невидимых граней", default_value=True)

    def _getCloneInstance(self, name: str, on_delete: Callable, on_clone: Callable) -> ObjFigure:
        return ObjFigure(name, on_delete, on_clone, self._model)

    def _getOrderedFaces(self) -> Iterable[_FaceData]:
        return self._model.faces

    def getMeshOffset(self) -> Vector3D:
        x, y = self._position_XY.getValue()
        return Vector3D(x / 100, y / 100, 0)

    def _vertexTransform(self, v: Vector3D) -> Vector3D:
        rx, ry = self._rotation_XY.getValue()

        return v.rotated_y(ry).rotated_x(rx).add(self.getMeshOffset())

    def _getProjectingVertices(self) -> Iterable[Vector3D]:
        return chain(*(f.transform(self._vertexTransform, self._face_culling.getValue()) for f in self._getOrderedFaces()))

    def _getCurrentProjector(self) -> Projector:
        return self._perspective_projector if self._use_perspective.getValue() else self._isometric_projector

    def _applyProjector(self) -> Iterable[tuple[float, float]]:
        projector = self._getCurrentProjector()
        vertices = self._getProjectingVertices()
        return map(projector.apply, vertices)

    def _generateVertices(self) -> Vertices:
        v = self._applyProjector()

        if v == ():
            return (), ()

        return zip(*v)

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)

        h = CollapsingHeader("3D", default_open=True)
        h.place(self)

        (
            h.add(self._rotation_XY)
            .add(self._face_culling)
            .add(self._position_XY)
            .add(self._use_perspective)
            # .add(self._sort_faces)
        )


class ObjLoader:

    def load(self, path: Path, on_delete: Callable, on_clone: Callable) -> Sequence[ObjFigure]:
        with open(path) as f:
            return self._processObj(f, on_delete, on_clone)

    def _processObj(self, stream: TextIO, on_delete: Callable, on_clone: Callable) -> Sequence[ObjFigure]:

        def err(msg: str) -> None:
            """err"""
            raise ValueError(f"Err : {self.__class__.__name__} : ( '{stream}' ) : {msg}")

        objects = list[ObjFigure]()
        current_model: Optional[_ModelData] = None

        v_index_offset = 1
        n_index_offset = 1

        for index, line in enumerate(stream):
            parts = line.strip().split()

            if not parts:
                continue

            match parts[0]:
                case 'o':
                    if current_model is not None:
                        v_index_offset += len(current_model.vertices)
                        n_index_offset += len(current_model.normals)
                        current_model.sortFaces()

                    current_model = _ModelData(list(), list(), list())
                    objects.append(ObjFigure(parts[1], on_delete, on_clone, current_model))

                case 'v':
                    if current_model is None:
                        err(f"obj not selected (v) - at {index}")

                    current_model.vertices.append(Vector3D.fromParts(parts[1:4]))

                case 'vn':
                    if current_model is None:
                        err(f"obj not selected (n) at {index}")

                    current_model.normals.append(Vector3D.fromParts(parts[1:4]))

                case 'f':
                    if current_model is None:
                        err(f"obj not selected (f) at {index}")

                    face = _FaceData.parse(parts[1:], current_model, v_index_offset, n_index_offset)

                    current_model.faces.append(face)

        current_model.sortFaces()

        return objects
