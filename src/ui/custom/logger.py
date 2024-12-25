from io import StringIO

from ui.abc import ItemID
from ui.abc import Placeable
from ui.dpg.impl import Button
from ui.dpg.impl import Text


class LoggerWidget(StringIO, Placeable):

    def __init__(self) -> None:
        super().__init__()
        self._text = Text("Logger")

    def placeRaw(self, parent_id: ItemID) -> None:
        Button("Clear", self.clearLogs).placeRaw(parent_id)
        self._text.placeRaw(parent_id)

    def clearLogs(self) -> None:
        """Очистить лог"""
        self._text.setValue("")

    def write(self, message: str):
        """Записать и отобразить"""
        self._text.setValue(self.getvalue())
        return super().write(message)
