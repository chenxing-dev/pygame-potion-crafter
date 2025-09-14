

from constants import PLAYER_NAME
from entities.entity import Entity


class Door(Entity):
    def __init__(self, x, y, char, color, name):
        super().__init__(x, y, char, color, name)

    def use(self, entities):
        entities.remove(self)
        return f"{PLAYER_NAME} opens the door."
