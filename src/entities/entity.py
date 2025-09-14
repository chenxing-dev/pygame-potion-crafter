from typing import Optional
from entities.base import GameObject
from entities.item import Item


class Entity(GameObject):
    """游戏中的实体类，结合了Reference的位置特性和Item的可交互特性"""

    def __init__(self, e_id: str, name: str, char: str, color: tuple, description: str = "", blocks=False, item: Optional['Item'] = None):
        super().__init__(e_id, name, description)
        self.char = char
        self.color = color
        self.blocks = blocks
        self.item = item  # 如果这不是None，那么这个实体代表一个可拾取的物品
        # 注意：Entity不存储位置信息，当它在地图上时，会有一个对应的Reference
