from os import PathLike
from pathlib import Path
from typing import BinaryIO
from typing import Iterable

from bytelang.compiler import ByteLangCompiler
from bytelang.core.results.compile.abc import CompileResult
from bytelang.tools.string import FixedStringIO
from bytelang.utils import LogFlag
from gen.codegen import CodeGenerator
from gen.enums import MarkerTool
from gen.enums import PlannerMode
from gen.trajectory import MovementPreset
from gen.trajectory import Trajectory


class CodeWriter:
    """"""

    @staticmethod
    def simpleSetup(setup_folder: PathLike | str, code_generator: CodeGenerator):
        setup_folder = Path(setup_folder)
        return CodeWriter(
            code_generator,
            ByteLangCompiler.simpleSetup(setup_folder / "bytelang")
        )

    def __init__(self, code_generator: CodeGenerator, bytelang: ByteLangCompiler) -> None:
        self.__code_generator = code_generator
        self.__bytelang = bytelang

    def run(self, trajectories: Iterable[Trajectory], bytecode_stream: BinaryIO, log_flag: LogFlag = LogFlag.ALL) -> CompileResult:
        stream = FixedStringIO()
        self.__code_generator.write(stream, trajectories)

        stream.seek(0)

        return self.__bytelang.compile(stream, bytecode_stream, log_flag)


def _test(output_path: str):
    c = CodeGenerator(
        MovementPreset(
            PlannerMode.ACCEL, 100, 50
        ),
        MovementPreset(
            PlannerMode.SPEED, 60, 0
        )
    )
    writer = CodeWriter.simpleSetup(r"A:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp\res", c)

    from gen.vertex import VertexGenerator
    vx, vy = VertexGenerator.nGon(6, 1)

    def f(i):
        return tuple(int(j * 200) for j in i)

    trajectories = (
        Trajectory(f(vx), f(vy), MarkerTool.RIGHT, True),
    )

    with open(output_path, "wb") as bytecode_stream:
        result = writer.run(trajectories, bytecode_stream)
        print(result.getMessage())


if __name__ == "__main__":
    _test(r"test.blc")
