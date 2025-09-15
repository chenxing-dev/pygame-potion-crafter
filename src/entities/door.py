from entities.reference import Reference


class Door(Reference):
    def __init__(self, door_id, name, x, y, char, color, description="A sturdy door.", locked=False, key_id=None):
        super().__init__(door_id, name, x, y, char, color, description, blocks=True)
        self.locked = locked
        self.key_id = key_id  # The ID of the key item that can unlock this door

    def activate(self):
        """Open the door"""
        if not self.blocks:
            return
        self.blocks = False
        self.char = ' '
        return f"You open the {self.name}."
