from entities.entity import Entity


class Item(Entity):
    def __init__(self, e_id: str, x: int, y: int, char: str, color: str, name: str):
        super().__init__(e_id, x, y, char, color, name, blocks=False)
