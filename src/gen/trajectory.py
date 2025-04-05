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

    planner_mode: int
    """Режим планировщика"""

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
        agent.setProfile(settings.getProfileByIndex(self.planner_mode))

        for x, y in zip(x_positions, y_positions):
            agent.step(x, y)

        agent.setProfile(settings.free_move_profile)
        agent.setTool(MarkerTool.NONE)

        agent.note(f"Trajectory : '{self.name}' End")
