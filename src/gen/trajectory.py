from dataclasses import dataclass
from typing import ClassVar
from typing import Optional
from typing import Sequence


@dataclass(frozen=True, kw_only=True)
class Trajectory:
    """Траектория перемещения"""

    MAX_TOOL_ID: ClassVar[int] = 3
    MAX_SPEED: ClassVar[int] = 10

    x_positions: Sequence[int]
    """Позиции перемещений X"""
    y_positions: Sequence[int]
    """Позиции перемещений Y"""
    tool_id: int
    """Инструмент печати"""
    movement_speed: int
    """Скорость перемещения"""
