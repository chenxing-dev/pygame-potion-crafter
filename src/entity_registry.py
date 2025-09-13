from entities import Actor, Item, Tool
import colors as COLOR

ENTITY_REGISTRY = {
    ")": (Tool, COLOR.GREEN, "Hammer", 0, 0),
}


# Generic entity classes
def create_entity(symbol, x, y):
    if symbol not in ENTITY_REGISTRY:
        return None

    cls, color, name, hp, damage = ENTITY_REGISTRY[symbol]

    if issubclass(cls, Actor):
        return cls(x, y, symbol, color, name, hp, damage)
    elif issubclass(cls, Item):
        # Special handling for item subtypes
        if cls == Tool:
            return Tool(x, y, symbol, color, name)
        else:
            value = hp  # hp used as value for items
            return cls(x, y, symbol, color, name, value)
    else:
        return cls(x, y, symbol, color, name)
