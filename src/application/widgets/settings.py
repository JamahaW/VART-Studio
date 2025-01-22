from gen.movementprofile import MovementProfile
from gen.settings import GeneratorSettings
from ui.widgets.abc import ItemID
from ui.widgets.dpg.impl import CollapsingHeader
from ui.widgets.dpg.impl import SliderInt


class ProfileWidget(CollapsingHeader):

    def __init__(self, profile: MovementProfile) -> None:
        super().__init__(f"Параметры {profile.name}")
        self._profile = profile

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        speed_slider = SliderInt("Скорость (мм/с)", self._onSpeed, value_range=MovementProfile.SPEED_RANGE.asTuple(), default_value=self._profile.speed)
        accel_slider = SliderInt("Ускорение (мм/с^2)", self._onAccel, value_range=MovementProfile.ACCEL_RANGE.asTuple(), default_value=self._profile.accel)
        self.add(speed_slider).add(accel_slider)

    def _onSpeed(self, speed: int) -> None:
        self._profile.speed = speed

    def _onAccel(self, accel: int) -> None:
        self._profile.accel = accel


class CodeGeneratorSettngsWidget(CollapsingHeader):

    def __init__(self, settings: GeneratorSettings) -> None:
        super().__init__("Общие Настройки", default_open=True)
        self.settings = settings

    def placeRaw(self, parent_id: ItemID) -> None:
        super().placeRaw(parent_id)
        self.add(ProfileWidget(self.settings.free_move_profile))
        self.add(ProfileWidget(self.settings.long_line_profile))
        self.add(ProfileWidget(self.settings.short_curve_profile))
