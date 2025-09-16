from entities.game_object import ObjectType
from entities.physical_object import PhysicalObject


class Static(PhysicalObject):
    """静态物体（墙壁、地板等）"""

    def __init__(self, static_id: str, char: str, color: tuple, blocks: bool = True):
        super().__init__(static_id, ObjectType.STATIC, blocks=blocks, interactable=False)
        self.char = char
        self.color = color

    def __str__(self):
        return self.id
