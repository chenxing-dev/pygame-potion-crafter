from typing import Dict, List
from data.items import item_registry


class Inventory:
    """库存系统"""

    def __init__(self) -> None:
        self.items: Dict[str, int] = {}  # item_id -> quantity

    def add_item(self, item_id: str, quantity: int = 1) -> bool:
        """添加物品到库存"""
        item = item_registry.get_item(item_id)
        if not item:
            return False

        if item.stackable:
            current_quantity = self.items.get(item_id, 0)
            if current_quantity + quantity > item.max_stack:
                return False  # 超过堆叠上限
            self.items[item_id] = self.items.get(item_id, 0) + quantity
        else:
            # 对于不可堆叠物品，每个占一个槽位
            for _ in range(quantity):
                # 为每个不可堆叠物品创建唯一ID
                unique_id = f"{item_id}_{len(self.items)}"
                self.items[unique_id] = 1

        return True

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """从库存移除物品"""
        if item_id not in self.items:
            return False

        item = item_registry.get_item(item_id)
        if not item:
            return False

        if item.stackable:
            if self.items[item_id] < quantity:
                return False

            self.items[item_id] -= quantity
            if self.items[item_id] <= 0:
                del self.items[item_id]
        else:
            # 对于不可堆叠物品，需要找到指定数量的实例
            items_to_remove = []
            for inv_item_id in list(self.items.keys()):
                if inv_item_id.startswith(item_id + "_"):
                    items_to_remove.append(inv_item_id)
                    if len(items_to_remove) >= quantity:
                        break

            if len(items_to_remove) < quantity:
                return False

            for inv_item_id in items_to_remove:
                del self.items[inv_item_id]

        return True

    def get_quantity(self, item_id: str) -> int:
        """获取指定物品的数量"""
        if item_id not in self.items:
            return 0

        item = item_registry.get_item(item_id)
        if not item:
            return 0

        return self.items[item_id]

    def get_display_list(self) -> List[str]:
        """获取库存中所有物品的列表（用于显示）"""
        result = []
        stackable_items = {}

        # 首先处理可堆叠物品
        stackable_items = {}
        for item_id, quantity in self.items.items():
            item = item_registry.get_item(item_id)
            if item and item.stackable:
                stackable_items[item_id] = quantity

        # 添加可堆叠物品到结果
        for item_id, quantity in stackable_items.items():
            item = item_registry.get_item(item_id)
            if item:
                if quantity > 1:
                    result.append(item.name)
                else:
                    result.append(f"{item.name} x{quantity}")

        # 添加不可堆叠物品到结果
        for item_id in self.items:
            item = item_registry.get_item(item_id)
            if item and not item.stackable:
                result.append(item.name)

        return result

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """检查是否有足够数量的指定物品"""
        return self.get_quantity(item_id) >= quantity
