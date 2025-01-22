from dataclasses import dataclass
from typing import BinaryIO
from typing import Iterable

from bytelang.compiler import ByteLangCompiler
from bytelang.core.results.compile.abc import CompileResult
from bytelang.tools.string import FixedStringIO
from bytelang.utils import LogFlag
from gen.agents import LowLevelAgent
from gen.agents import MacroAgent
from gen.enums import MarkerTool
from gen.enums import PlannerMode
from gen.settings import GeneratorSettings
from gen.movementprofile import MovementProfile
from gen.trajectory import Trajectory


@dataclass
class CodeWriter:
    """Запись байткода"""

    _settings: GeneratorSettings
    _bytelang: ByteLangCompiler

    def run(self, trajectories: Iterable[Trajectory], bytecode_stream: BinaryIO, log_flag: LogFlag = LogFlag.ALL) -> CompileResult:
        stream = FixedStringIO()
        self._processAgent(MacroAgent(LowLevelAgent(stream), self._calcTotalStepCount(trajectories)), trajectories)
        stream.seek(0)
        print(stream.getvalue())
        return self._bytelang.compile(stream, bytecode_stream, log_flag)

    def _processAgent(self, agent: MacroAgent, trajectories: Iterable[Trajectory]):
        agent.prologue()

        for trajectory in trajectories:
            trajectory.run(agent, self._settings)

        agent.epilogue()

    @staticmethod
    def _calcTotalStepCount(trajectories: Iterable[Trajectory]) -> int:
        return sum(t.vertexCount() for t in trajectories)


def _test(output_path: str):
    settings = GeneratorSettings(
        MovementProfile("Free", PlannerMode.ACCEL, 100, 50),
        MovementProfile("Long", PlannerMode.ACCEL, 75, 25),
        MovementProfile("Short", PlannerMode.SPEED, 50, 0)
    )
    writer = CodeWriter(settings, ByteLangCompiler.simpleSetup(r"A:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp\res\bytelang"))

    from gen.vertex import VertexGenerator
    vx, vy = VertexGenerator.nGon(6, 1)
    vx1, vy1 = VertexGenerator.nGon(12, 1)

    def f(i):
        return tuple(int(j * 200) for j in i)

    trajectories = (
        Trajectory("Test", f(vx), f(vy), MarkerTool.RIGHT, True),
        Trajectory("Test", f(vx1), f(vy1), MarkerTool.RIGHT, True),
    )

    with open(output_path, "wb") as bytecode_stream:
        result = writer.run(trajectories, bytecode_stream)
        print(result.getMessage())


if __name__ == "__main__":
    _test(r"test.blc")
