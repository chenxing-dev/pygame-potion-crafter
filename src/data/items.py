from typing import Dict, Optional
from entities import Item


class ItemRegistry:
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


# 全局物品注册实例
item_registry = ItemRegistry()
