from entities.base import GameObject


class Item(GameObject):
    """可拾取的物品实体"""

    def __init__(self, item_id: str, name: str, description: str = "", stackable: bool = True, max_stack: int = 99):
        super().__init__(item_id, name, description)
        # 物品不存储位置信息，当它们在地图上时，会有一个对应的Reference对象
        self.stackable = stackable
        self.max_stack = max_stack
