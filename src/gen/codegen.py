from dataclasses import dataclass
from typing import Iterable
from typing import TextIO

from gen.enums import MarkerTool
from gen.enums import PlannerMode
from gen.trajectory import MovementPreset
from gen.trajectory import Trajectory

_BEGIN = """

# CODE BEGIN
    .env vart_esp32
    
    delay_ms 1000
    set_active_tool 0

"""

_END = """
    set_planner_mode 2
    set_position 0 0
    
    delay_ms 1000
    set_active_tool 0
    
    quit
# CODE END
"""


@dataclass
class CodeGenerator:
    accel_preset: MovementPreset
    speed_preset: MovementPreset

    def write(self, stream: TextIO, trajectories: Iterable[Trajectory]) -> None:
        stream.write(_BEGIN)

        for trajectory in trajectories:
            p = self.accel_preset if trajectory.accel_profile else self.speed_preset
            trajectory.write(stream, p)

        stream.write(_END)


def _test():
    from io import StringIO

    c = CodeGenerator(
        MovementPreset(
            PlannerMode.ACCEL, 150, 50
        ),
        MovementPreset(
            PlannerMode.SPEED, 80, 0
        )
    )

    s = StringIO()

    t = (
        Trajectory(
            (10, 20, 30),
            (10, 20, 40),
            MarkerTool.LEFT,
            True
        ),
        Trajectory(
            (100, 0, -100),
            (0, 0, 0),
            MarkerTool.RIGHT,
            False
        )
    )

    c.write(s, t)

    print(s.getvalue())


if __name__ == '__main__':
    _test()
