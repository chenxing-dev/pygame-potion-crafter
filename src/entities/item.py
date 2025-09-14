from entities.game_object import GameObject


class Item(GameObject):
    """物品类，可被拾取和存储在库存中"""

    def __init__(self, item_id: str, name: str, description: str = "", stackable: bool = True, max_stack: int = 99):
        super().__init__(item_id, name, description)
        # 物品不存储位置信息，当它们在地图上时，会有一个对应的Reference对象
        self.stackable = stackable
        self.max_stack = max_stack

    def __str__(self):
        return self.name
