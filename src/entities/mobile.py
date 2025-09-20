from typing import TYPE_CHECKING
from core import Serializable


if TYPE_CHECKING:
    from entities.npc import NPC
    from entities.player import Player
    from entities.reference import Reference
    from game import Game


class Mobile(Serializable):
    """可移动的实体，有位置信息且可以移动"""

    def __init__(self, x: int, y: int, reference: 'Reference[NPC|Player]'):
        super().__init__()
        self.x = x
        self.y = y
        self.reference = reference

        self.hp = self.reference.object_data.max_hp or 10

        self._serializable_exclude.add('reference')  # 避免递归序列化

    def move(self, dx: int, dy: int, game: 'Game'):
        """移动实体"""
        if game.world is None:
            print("没有游戏世界，无法移动")
            return
        new_x = self.x + dx
        new_y = self.y + dy

        if game.world.is_within_bounds(new_x, new_y):
            # Move player and sync reference position
            self.x, self.y = new_x, new_y
            self.reference.x, self.reference.y = new_x, new_y
        else:
            print("移动超出边界")

    def greet(self, target: 'Reference') -> str | None:
        """Greet another actor and return result message"""
        return f"{self.reference.object_data.name} greets {target.object_data.name}!"

    def to_dict(self) -> dict:
        data = super().to_dict()
        # Avoid deep recursion by only storing reference ID
        data['reference'] = self.reference.id
        return data
