from dataclasses import dataclass
from typing import Callable, Dict, Optional

from entities.game_object import GameObject


@dataclass
class Activator(GameObject):
    """可交互对象，存储交互逻辑"""

    def __init__(self, activator_id: str, name: str, description: str, actions: Optional[Dict[str, Callable]] = None):
        super().__init__(activator_id, name, description)
        self.actions = actions

    def get_actions(self):
        """获取可用的动作列表"""
        if self.actions:
            return list(self.actions.keys())
        return []

    def activate(self, action_name: str, game) -> str | None:
        """执行动作"""
        if self.actions:
            action = self.actions.get(action_name)
            if action:
                return action(self, game)
        return None
