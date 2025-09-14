from entities.entity import Entity


class Door(Entity):
    def __init__(self, e_id, x, y, char, color, name):
        super().__init__(e_id, x, y, char, color, name, blocks=True)

    def activate(self):
        """Open the door"""
        if not self.blocks:
            return
        self.blocks = False
        self.char = ' '
        return f"You open the {self.name}."
