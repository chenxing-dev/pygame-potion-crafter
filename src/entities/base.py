from dataclasses import dataclass


@dataclass
class GameObject:
    """所有游戏对象的基类"""
    id: str
    name: str
    description: str = ""

    def __str__(self):
        return self.name
