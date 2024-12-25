from gen.settings import GeneratorSettings
from gen.trajectory import Trajectory
from ui.abc import ItemID
from ui.dpg.impl import CollapsingHeader
from ui.dpg.impl import InputInt
from ui.dpg.impl import SliderInt


class CodeGeneratorSettngsWidget(CollapsingHeader):

    def __init__(self, config: GeneratorSettings) -> None:
        super().__init__("Code Generator")
        self._config = config

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        c = self._config
        self.add(SliderInt("Default Speed", self._onSpeed, value_range=GeneratorSettings.getSpeedRange(), default_value=c.speed))
        self.add(SliderInt("End Speed (move home)", self._onEndSpeed, value_range=GeneratorSettings.getSpeedRange(), default_value=c.end_speed))
        self.add(InputInt("Tool None ID", self._onToolNone, value_range=(0, Trajectory.MAX_TOOL_ID), default_value=c.tool_none))
        self.add(InputInt("Disconnect Distance (mm)", self._onDisconnectDist, value_range=(0, GeneratorSettings.MAX_DISCONNECT_DISTANCE_MM), default_value=c.disconnect_distance_mm))
        self.add(InputInt("Tool Change Duration (ms)", self._onToolChangeDuration, value_range=(0, GeneratorSettings.MAX_TOOL_CHANGE_DURATION_MS), default_value=c.tool_change_duration_ms))

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
