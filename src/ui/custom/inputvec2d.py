from typing import Callable

from ui.dpg.impl import Group


class InputVector2D(Group):

    def __init__(self, handler: Callable[[tuple[int, int]], None]):
        super().__init__()
