from dataclasses import dataclass
from typing import ClassVar


@dataclass(kw_only=True)
class GeneratorSettings:
    """Настройки генерации кода"""

    MIN_SPEED: ClassVar[int] = 1
    MAX_SPEED: ClassVar[int] = 16

    MAX_DISCONNECT_DISTANCE_MM: ClassVar[int] = 50
    MAX_TOOL_CHANGE_DURATION_MS: ClassVar[int] = 5000

    @classmethod
    def getSpeedRange(cls) -> tuple[int, int]:
        """Получить минимальную и максимальную скорость перемещения"""
        return cls.MIN_SPEED, cls.MAX_SPEED

    speed: int
    """Скорость перемещения"""
    end_speed: int
    """Скорость перемещения при перемещении домой"""
    tool_none: int
    """код неактивного инструмента"""
    disconnect_distance_mm: int
    """критическое расстояние между вершинами"""
    tool_change_duration_ms: int
    """Задержка при смене инструмента"""
