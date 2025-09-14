from typing import Dict, Optional
from entities import Item


class ItemRegistry:
    """物品注册表"""

    def __init__(self):
        self.items: Dict[str, Item] = {}

    def register_item(self, item: Item):
        """注册物品"""
        if item.id in self.items:
            raise ValueError(f"Item with id {item.id} is already registered.")
        self.items[item.id] = item

    def get_item(self, item_id: str) -> Optional[Item]:
        """获取物品"""
        return self.items.get(item_id)

    def get_all_items(self) -> Dict[str, Item]:
        """获取所有注册的物品"""
        return self.items.copy()


# 创建全局物品注册表
item_registry = ItemRegistry()

# 注册物品
item_registry.register_item(Item("silver_leaf", "Silver Leaf",
                            "A shiny leaf with natural cleaning properties.", True, 99))
item_registry.register_item(Item("lemon_fruit", "Lemon Fruit",
                            "A sour citrus fruit with acidic properties.", True, 99))
item_registry.register_item(Item("glowshroom", "Glowshroom",
                            "A bioluminescent mushroom that glows in the dark.", True, 99))
item_registry.register_item(Item(
    "moon_dew", "Moon Dew", "Dew collected under moonlight, imbued with lunar energy.", True, 99))
item_registry.register_item(Item(
    "glowing_moss", "Glowing Moss", "Moss that emits a soft, ethereal glow.", True, 99))
item_registry.register_item(Item("cleaning_gloop", "Cleaning Gloop",
                            "A viscous cleaning solution for removing stubborn residues.", True, 10))
item_registry.register_item(
    Item("pruning_shears", "Pruning Shears", "A tool for harvesting plants.", False))
