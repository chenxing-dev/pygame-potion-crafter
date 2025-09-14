from typing import Callable
from entities.entity import Entity


class Activator(Entity):
    def __init__(self, e_id, name, char, color, description, actions: dict[str, Callable]):
        super().__init__(e_id, char, color, description, name)
        self.actions = actions

    def get_actions(self):
        return list(self.actions.keys())

    def activate(self, action_name: str, game):
        action = self.actions.get(action_name)
        if action:
            return action(self, game)
        return None
