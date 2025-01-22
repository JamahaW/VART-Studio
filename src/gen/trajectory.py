from dataclasses import dataclass
from typing import Iterable
from typing import TextIO

from gen.enums import MarkerTool
from gen.enums import PlannerMode


@dataclass(frozen=True)
class MovementPreset:
    """ПредНастройка перемещения"""

    mode: PlannerMode
    """Режим планировщика"""

    speed: int
    """Заданная скорость"""

    accel: int
    """Заданное ускорение"""


_BEGIN = """
# TRAJECTORY BEGIN
    set_planner_mode {mode}
    set_speed {speed}
    set_accel {accel}
    set_active_tool 0
"""

_ON_POSITION = "set_position {x} {y}\n"

_END = """
    set_active_tool 0
# TRAJECTORY END

"""


@dataclass(frozen=True)
class Trajectory:
    """Траектория - непрерывная кривая"""

    x_positions: Iterable[int]
    """Позиции перемещений X"""

    y_positions: Iterable[int]
    """Позиции перемещений Y"""

    tool: MarkerTool
    """Инструмент печати"""

    accel_profile: bool
    """Использовать профиль с ускорением"""

    def write(self, stream: TextIO, preset: MovementPreset) -> None:
        stream.write(_BEGIN.format(mode=preset.mode, speed=preset.speed, accel=preset.accel))

        x_start, *x_positions = self.x_positions
        y_start, *y_positions = self.y_positions

        stream.write(_ON_POSITION.format(x=x_start, y=y_start))
        stream.write(f"set_active_tool {self.tool}\n")

        for x, y in zip(x_positions, y_positions):
            stream.write(_ON_POSITION.format(x=x, y=y))

        stream.write(_END.format(none_tool=MarkerTool.NONE))


def _test():
    t = Trajectory(
        (0, 10, 20, 30, 40),
        (50, 40, 30, 20, 10),
        MarkerTool.LEFT,
        True
    )

    from io import StringIO

    s = StringIO()
    m = MovementPreset(PlannerMode.ACCEL, 150, 75)

    t.write(s, m)

    print(s.getvalue())


if __name__ == '__main__':
    _test()
