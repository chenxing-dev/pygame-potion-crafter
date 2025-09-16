from entities.physical_object import PhysicalObject, ObjectType


class Item(PhysicalObject):
    """物品类，可被拾取和存储在库存中"""

    def __init__(self, item_id: str, name: str, char: str, color: tuple):
        super().__init__(item_id, object_type=ObjectType.ITEM, blocks=False, interactable=True)
        # 物品不存储位置信息，当它们在地图上时，会有一个对应的Reference对象
        self.name = name
        self.char = char
        self.color = color

    def __str__(self):
        return self.name
