from dataclasses import dataclass
from typing import Callable, Dict, Optional

from entities.game_object import ObjectType
from entities.physical_object import PhysicalObject


@dataclass
class Activator(PhysicalObject):
    """可交互对象，存储交互逻辑"""

    def __init__(self, activator_id: str, name: str, char: str, color: tuple, actions: Optional[Dict[str, Callable]] = None):
        super().__init__(activator_id, object_type=ObjectType.ACTIVATOR,
                         blocks=True, interactable=True)
        self.name = name
        self.char = char
        self.color = color
        self.actions = actions if actions else {}

    def get_actions(self):
        """获取可用的动作列表"""
        if self.actions:
            return list(self.actions.keys())
        return []
