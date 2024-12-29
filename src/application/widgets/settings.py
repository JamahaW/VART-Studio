from gen.settings import GeneratorSettings
from gen.trajectory import Trajectory
from ui.widgets.abc import ItemID
from ui.widgets.dpg.impl import CollapsingHeader
from ui.widgets.dpg.impl import InputInt
from ui.widgets.dpg.impl import SliderInt


class CodeGeneratorSettngsWidget(CollapsingHeader):

    def __init__(self, config: GeneratorSettings) -> None:
        super().__init__("Генератор Байт-Кода", default_open=True)
        self._config = config

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        c = self._config
        self.add(SliderInt("Скорость печати по умолчанию", self._onSpeed, value_range=GeneratorSettings.getSpeedRange(), default_value=c.speed))
        self.add(SliderInt("Скорость перемещения домой", self._onEndSpeed, value_range=GeneratorSettings.getSpeedRange(), default_value=c.end_speed))
        self.add(InputInt("Инструмент без печати", self._onToolNone, value_range=(0, Trajectory.MAX_TOOL_ID), default_value=c.tool_none))
        self.add(InputInt("Расстояние отсоединения (мм)", self._onDisconnectDist, value_range=(0, GeneratorSettings.MAX_DISCONNECT_DISTANCE_MM), default_value=c.disconnect_distance_mm))
        self.add(InputInt("Пауза после смены инструмента (мс)", self._onToolChangeDuration, value_range=(0, GeneratorSettings.MAX_TOOL_CHANGE_DURATION_MS), default_value=c.tool_change_duration_ms))

    def _onSpeed(self, value: int):
        self._config.speed = value

    def _onEndSpeed(self, value: int):
        self._config.end_speed = value

    def _onToolNone(self, tool_id: int):
        self._config.tool_none = tool_id

    def _onDisconnectDist(self, dist: int):
        self._config.disconnect_distance_mm = dist

    def _onToolChangeDuration(self, ms: int):
        self._config.tool_change_duration_ms = ms
