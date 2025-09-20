from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union, TypeVar, Generic
from core import Serializable
from entities.activator import Activator
from entities.door import Door


if TYPE_CHECKING:
    from entities.physical_object import PhysicalObject
    from entities.npc import NPC
    from entities.mobile import Mobile
    from entities.player import Player, MobilePlayer
    from game import Game


T_co = TypeVar('T_co', bound='PhysicalObject', covariant=True)


@dataclass
class Reference(Generic[T_co], Serializable):
    """地图上的实体引用，有位置信息和外观"""

    def __init__(self, x: int, y: int, object_data: T_co):
        super().__init__()
        self.id = f"{object_data.id}_{x}_{y}"
        self.x = x
        self.y = y
        self.object_data = object_data  # 关联的实体对象，如Player
        self.mobile: 'Mobile | MobilePlayer | None' = None  # 如果是可移动实体，则关联其移动组件

        # Door specific attributes
        self.locked = False  # 默认门是未锁的
        self.key_id = None  # 默认没有钥匙ID
        self.destination_map: Optional[str] = None
        self.destination_pos: Optional[tuple] = None

    def __str__(self):
        return self.id

    def activate(self, game: 'Game', action_name: str | None = None) -> Union[str, None]:
        """激活该引用的对象，执行其动作"""
        if self.object_data.interactable is False:
            return
        if isinstance(self.object_data, Door):
            print("activate door")
            if self.locked:
                return f"The {self.object_data.name} is locked."
            if not self.object_data.blocks:
                return
            self.object_data.blocks = False
            self.object_data.char = self.object_data.open_char
            return f"You open the {self.object_data.name}."
        if isinstance(self.object_data, Activator):
            actions = self.object_data.get_actions()
            if actions:
                if not action_name:
                    action_name = actions[0]  # 默认执行第一个动作
                return self.object_data.actions[action_name](game)
