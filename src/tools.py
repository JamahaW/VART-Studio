from dataclasses import dataclass


@dataclass
class Range[T]:
    """Диапазон значений"""

    min: T
    """Минимальное из этого диапазона"""
    max: T
    """Максимальное"""

    def asTuple(self) -> tuple[T, T]:
        """Представить в виде кортежа"""
        return self.min, self.max

    def clamp(self, value: T) -> T:
        """Получить значение ограниченное диапазоном"""
        return min(self.max, max(self.min, value))
