from dataclasses import dataclass
from typing import ClassVar
from typing import Iterable


@dataclass(frozen=True, kw_only=True)
class Trajectory:
    """Траектория перемещения"""

    MAX_TOOL_ID: ClassVar[int] = 3

    x_positions: Iterable[int]
    """Позиции перемещений X"""
    y_positions: Iterable[int]
    """Позиции перемещений Y"""
    tool_id: int
    """Инструмент печати"""
    movement_speed: int
    """Скорость перемещения"""
