from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import BinaryIO
from typing import Iterable

from bytelang.compiler import ByteLangCompiler
from bytelang.core.results.compile.abc import CompileResult
from bytelang.tools.string import FixedStringIO
from bytelang.utils import LogFlag
from gen.code import CodeGenerator
from gen.settings import GeneratorSettings
from gen.trajectory import Trajectory


class CodeWriter:
    """"""

    @staticmethod
    def simpleSetup(setup_folder: PathLike | str) -> CodeWriter:
        setup_folder = Path(setup_folder)
        return CodeWriter(
            CodeGenerator.load(setup_folder / "code"),
            ByteLangCompiler.simpleSetup(setup_folder / "bytelang")
        )

    def __init__(self, code_generator: CodeGenerator, bytelang: ByteLangCompiler) -> None:
        self.__code_generator = code_generator
        self.__bytelang = bytelang

    def run(self, config: GeneratorSettings, contours: Iterable[Trajectory], bytecode_stream: BinaryIO, log_flag: LogFlag = LogFlag.ALL) -> CompileResult:
        stream = FixedStringIO()
        self.__code_generator.run(stream, config, contours)

        stream.seek(0)

        return self.__bytelang.compile(stream, bytecode_stream, log_flag)


def test(output_path: str):
    writer = CodeWriter.simpleSetup(r"A:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp\res")

    config = GeneratorSettings(
        speed=5,
        end_speed=10,
        tool_none=0,
        disconnect_distance_mm=4,
        tool_change_duration_ms=200,
    )

    trajectories = (
        Trajectory(x_positions=range(5), y_positions=range(5), tool_id=1, movement_speed=5),
    )

    with open(output_path, "wb") as bytecode_stream:
        result = writer.run(config, trajectories, bytecode_stream, LogFlag.PROGRAM_SIZE | LogFlag.COMPILATION_TIME | LogFlag.BYTECODE)
        print(result.getMessage())


if __name__ == "__main__":
    test(r"A:\Projects\Vertical-Art-Robot-Technology\Code\VART-DesktopApp\res\out\test.blc")
