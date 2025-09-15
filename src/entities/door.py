from config import COLOR
from entities.game_object import GameObject, ObjectType


class Door(GameObject):
    def __init__(self, door_id, name, char="+", color=COLOR.SADDLE_BROWN, description="A sturdy door.", locked=False, key_id=None):
        super().__init__(door_id, object_type=ObjectType.DOOR, blocks=True, interactable=True)
        self.name = name
        self.char = char
        self.color = color
        self.description = description
        self.locked = locked
        self.key_id = key_id  # The ID of the key item that can unlock this door

    def activate(self):
        """Open the door"""
        if not self.blocks:
            return
        self.blocks = False
        self.char = ' '
        return f"You open the {self.name}."
