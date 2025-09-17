from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from entities import PhysicalObject


class ObjectManager:
    """物品注册表"""

    def __init__(self):
        self.objects: Dict[str, 'PhysicalObject'] = {}

    def add_object(self, obj: 'PhysicalObject'):
        """注册物品"""
        if obj.id in self.objects:
            raise ValueError(f"Object with id {obj.id} is already registered.")
        self.objects[obj.id] = obj

    def get_object(self, object_id: str) -> Optional['PhysicalObject']:
        """获取物品"""
        return self.objects.get(object_id)

    def get_all_objects(self) -> Dict[str, 'PhysicalObject']:
        """获取所有注册的物品"""
        return self.objects.copy()


object_manager = ObjectManager()
