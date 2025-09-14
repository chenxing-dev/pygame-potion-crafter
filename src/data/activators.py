from entities import Activator


class ActivatorRegistry:
    """交互实体注册表"""

    def __init__(self):
        self._activators = {}

    def register_activator(self, activator: Activator):
        """注册交互实体"""
        self._activators[activator.id] = activator

    def get_activator(self, activator_id: str):
        """获取交互实体"""
        return self._activators.get(activator_id)

    def get_all_activators(self):
        """获取所有交互实体"""
        return self._activators.copy()


# 创建全局交互实体注册表
activator_registry = ActivatorRegistry()

# 定义酿造台的回调函数


def examine_brewing_station(_, game):
    if game.world_state.get("brewing_station_cleaned", False):
        return "The brewing station is clean and ready to use."
    else:
        return "The brewing station is covered in dust and residue. It needs cleaning."


def clean_brewing_station(_, game):
    if game.player.inventory.has_item("cleaning_gloop", 1):
        game.world_state["brewing_station_cleaned"] = True
        return "You apply the cleaning gloop to the pipes.\n" +\
            "It begins dissolving the blockage."
    return "You need a cleaning solution to clear these pipes."


activator_registry.register_activator(Activator(
    "brewing_station",
    "Brewing Station",
    "A large station for brewing potions and extracts.",
    {
        "examine": examine_brewing_station,
        "clean": clean_brewing_station
    }
))
