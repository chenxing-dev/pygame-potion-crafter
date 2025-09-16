from entities.game_object import ObjectType
from entities.inventory import Inventory
from entities.physical_object import PhysicalObject


class NPC(PhysicalObject):
    """行动者类，可以执行动作并有库存"""

    def __init__(self, actor_id: str, name: str, char: str, color: tuple):
        super().__init__(actor_id, object_type=ObjectType.NPC, blocks=True, interactable=True)
        self.name = name
        self.char = char
        self.color = color
        self.inventory = Inventory()
        self.max_hp = 10

    def get_inventory_display(self):
        """获取用于显示的库存列表"""
        return self.inventory.get_display_list()
