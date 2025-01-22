from dataclasses import dataclass

from gen.movementprofile import MovementProfile


@dataclass
class GeneratorSettings:
    """Настройки генератора"""

    free_move_profile: MovementProfile
    """Профиль перемещения без рисования (свободное перемещение)"""

    long_line_profile: MovementProfile
    """Профиль перемещения для рисования длинных линий (Полигоны и т.п.)"""

    short_curve_profile: MovementProfile
    """Профиль перемещения для рисования кривых (Множество точек рядом)"""
