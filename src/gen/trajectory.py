from dataclasses import dataclass
from typing import Iterable

from gen.agents import MacroAgent
from gen.enums import MarkerTool
from gen.settings import GeneratorSettings


@dataclass(frozen=True)
class Trajectory:
    """Траектория - непрерывная кривая"""

    name: str
    """Наименование траектории для заметок"""

    x_positions: Iterable[int]
    """Позиции перемещений X"""

    y_positions: Iterable[int]
    """Позиции перемещений Y"""

    tool: MarkerTool
    """Инструмент печати"""

    accel_profile: bool
    """Использовать профиль с ускорением"""

    def vertexCount(self) -> int:
        """Количество вершин"""
        return len(tuple(self.x_positions))

    def run(self, agent: MacroAgent, settings: GeneratorSettings):
        """Использовать агента для преодоления траектории"""

        x_start, *x_positions = self.x_positions
        y_start, *y_positions = self.y_positions

        agent.note(f"Trajectory : '{self.name}' Begin")

        agent.setProfile(settings.free_move_profile)
        agent.setTool(MarkerTool.NONE)

        agent.step(x_start, y_start)

        agent.setTool(self.tool)
        agent.setProfile(settings.long_line_profile if self.accel_profile else settings.short_curve_profile)

        for x, y in zip(x_positions, y_positions):
            agent.step(x, y)

        agent.setTool(MarkerTool.NONE)
        agent.setProfile(settings.free_move_profile)

        agent.note(f"Trajectory : '{self.name}' End")
