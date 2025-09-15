from dataclasses import dataclass
from typing import Any
from entities.game_object import GameObject


@dataclass
class Reference(GameObject):
    """地图上的实体引用，有位置信息和外观"""

    def __init__(self, ref_id: str, name: str, x: int, y: int, char: str, color: tuple, description: str = "", blocks: bool = False, object_data: Any = None):
        super().__init__(ref_id, name, description)
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.blocks = blocks
        self.object_data = object_data  # 关联的实体对象，如Player

    def __str__(self):
        return self.name
