from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.game_object import GameObject


@dataclass
class Reference:
    """地图上的实体引用，有位置信息和外观"""

    def __init__(self, x: int, y: int, object_data: 'GameObject'):
        self.id = f"{object_data.id}_{x}_{y}"
        self.x = x
        self.y = y
        self.object_data = object_data  # 关联的实体对象，如Player

    def __str__(self):
        return self.id
