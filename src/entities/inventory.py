from typing import Dict, List
from core import Serializable
from entities.item import Item
from data.object_manager import object_manager


class Inventory(Serializable):
    """库存系统"""

    def __init__(self) -> None:
        super().__init__()
        self.object_manager = object_manager
        self.items: Dict[str, int] = {}  # item_id -> quantity

        self._serializable_exclude.add('object_manager')

    def add_item(self, item_id: str, quantity: int = 1) -> int:
        """添加物品到库存"""
        item = self.object_manager.get_object(item_id)
        if not item:
            return 0
        if not isinstance(item, Item):
            return 0

        self.items[item_id] = self.items.get(item_id, 0) + quantity

        return quantity

    def remove_item(self, item_id: str, quantity: int = 1) -> int:
        """从库存移除物品"""
        if item_id not in self.items:
            return False

        item = self.object_manager.get_object(item_id)
        if not item:
            return 0

        if self.items[item_id] < quantity:
            return 0

        self.items[item_id] -= quantity
        if self.items[item_id] <= 0:
            del self.items[item_id]

        return quantity

    def get_quantity(self, item_id: str) -> int:
        """获取指定物品的数量"""
        if item_id not in self.items:
            return 0

        item = self.object_manager.get_object(item_id)
        if not item:
            return 0

        return self.items[item_id]

    def get_display_list(self) -> List[str]:
        """获取库存中所有物品的列表（用于显示）"""
        result = []

        for item_id, quantity in self.items.items():
            item = self.object_manager.get_object(item_id)
            if item:
                # Narrow the type so the type checker knows .name exists
                if isinstance(item, Item):
                    result.append(f"{item.name} x{quantity}")

        return result

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """检查是否有足够数量的指定物品"""
        return self.get_quantity(item_id) >= quantity
