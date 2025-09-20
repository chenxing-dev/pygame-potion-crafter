from dataclasses import dataclass
from enum import Enum, auto
from core import Serializable


class ObjectType(Enum):
    """游戏对象类型枚举"""
    ACTIVATOR = auto()      # 可激活对象(工作台、炼金站等)
    ITEM = auto()           # 可拾取物品
    NPC = auto()            # 角色/NPC
    CONTAINER = auto()      # 容器
    DOOR = auto()           # 门
    STATIC = auto()         # 静态物体（墙壁、地板等）

    def to_dict(self):
        return self.name


@dataclass
class GameObject(Serializable):
    """所有游戏对象的基类"""

    def __init__(self, obj_id: str, object_type: ObjectType):
        super().__init__()
        self.id = obj_id
        self.object_type = object_type

    def __str__(self):
        return self.id
