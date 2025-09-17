from config import COLOR
from entities.game_object import ObjectType
from entities.physical_object import PhysicalObject


class Door(PhysicalObject):
    def __init__(self, door_id, name, char="+", color=COLOR.SADDLE_BROWN):
        super().__init__(door_id, object_type=ObjectType.DOOR, blocks=True, interactable=True)
        self.name = name
        self.color = color
        self.char = char
        self.close_char = self.char
        self.open_char = ' '
