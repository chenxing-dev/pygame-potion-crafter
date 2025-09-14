from config import COLOR
from entities import Activator, Actor, Door, Entity, Item, Reference, Tool
from data.items import item_registry


class EntityRegistry:
    """实体注册表"""

    def __init__(self):
        self._entities = {}

    def register_entity(self, entity_id: str, entity: Entity):
        """注册实体"""
        self._entities[entity_id] = entity
        return entity

    def get_entity(self, entity_id: str):
        """获取实体"""
        return self._entities.get(entity_id)

    def create_reference(self, entity_id: str, x: int, y: int) -> Reference | None:
        """根据实体ID创建地图参照物"""
        entity = self.get_entity(entity_id)
        if not entity:
            return None

        return Reference(
            ref_id=f"{entity_id}_{x}_{y}",
            name=entity.name,
            x=x,
            y=y,
            char=entity.char,
            color=entity.color,
            description=entity.description,
            blocks=entity.blocks
        )


# 创建全局实体注册表
entity_registry = EntityRegistry()

brewing_station_actions = {
    "examine": lambda _, __:
        "The main brewing station is clogged with a dark substance.\n" +
        "It looks like it needs to be cleaned out before it can be used.",
    "clean": lambda _, game: (
        "You apply the cleaning gloop to the pipes.\n" +
        "It begins dissolving the blockage." if "Cleaning Gloop" in game.player.get_inventory()
        else "You need a cleaning solution to clear these pipes."
    )
}


ENTITY_REGISTRY = {
    ")": (Tool, "hammer", "Hammer", COLOR.DARK_GREEN, "", None),
    "B": (Activator, "brewing_station", "Brewing Station", COLOR.DARK_RED, "The heart of the workshop, currently inactive.", brewing_station_actions),
    "+": (Door, "door", "Door", COLOR.SADDLE_BROWN, "", None),
    "%": (Door, "silver_leaf", "Silver Leaf", COLOR.DARK_GREEN, "A shiny leaf with natural cleaning properties.", None),
}


# Generic entity classes
def create_entity(symbol, x, y):
    if symbol not in ENTITY_REGISTRY:
        return None

    cls, e_id, name, color, description, actions = ENTITY_REGISTRY[symbol]

    if issubclass(cls, Activator):
        return entity_registry.register_entity("brewing_tower", Entity(e_id, name, symbol, color, description, actions))
    if issubclass(cls, Actor):
        return cls(e_id, name, x, y, symbol, color)
    if issubclass(cls, Item):
        entity_registry.register_entity("silver_leaf", Entity(
            "silver_leaf",
            "Silver Leaf",
            "%",
            (85, 107, 47),
            "A shiny leaf with natural cleaning properties.",
            False,
            item_registry.get_item("silver_leaf")
        ))
    return None
