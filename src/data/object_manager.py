from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from entities import PhysicalObject, Item, Tool


class ObjectManager:
    """物品注册表"""

    def __init__(self):
        self.objects: Dict[str, 'PhysicalObject | Item | Tool'] = {}

    def add_object(self, obj: 'PhysicalObject | Item | Tool'):
        """注册物品"""
        if obj.id in self.objects:
            raise ValueError(f"Object with id {obj.id} is already registered.")
        self.objects[obj.id] = obj

    def get_object(self, object_id: str) -> Optional['PhysicalObject | Item | Tool']:
        """获取物品"""
        return self.objects.get(object_id)

    def get_all_objects(self) -> Dict[str, 'PhysicalObject | Item | Tool']:
        """获取所有注册的物品"""
        return self.objects.copy()


object_manager = ObjectManager()
