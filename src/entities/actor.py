from entities.mobile import Mobile
from entities.inventory import Inventory


class Actor(Mobile):
    """行动者类，可以执行动作并有库存"""

    def __init__(self, actor_id: str, name: str, x: int, y: int, char: str, color: tuple, description: str = ""):
        super().__init__(actor_id, name, x, y, char, color, description, blocks=True)
        self.inventory = Inventory()
        self.max_hp = 10
        self.hp = self.max_hp

    def greet(self, target):
        """Greet another actor and return result message"""
        return f"{self.name} greets {target.name}!"
