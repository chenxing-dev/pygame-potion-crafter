
from entities.entity import Entity


class Item(Entity):
    def __init__(self, x, y, char, color, name):
        super().__init__(x, y, char, color, name, blocks=False)
