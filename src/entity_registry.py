from entities import Actor, Item, Tool, Door
import colors as COLOR

ENTITY_REGISTRY = {
    ")": (Tool, COLOR.DARK_GREEN, "Hammer"),
    "B": (Actor, COLOR.DARK_RED, "Animated Broom"),
    "+": (Door, COLOR.SADDLE_BROWN, "Door"),
}


# Generic entity classes
def create_entity(symbol, x, y):
    if symbol not in ENTITY_REGISTRY:
        return None

    cls, color, name = ENTITY_REGISTRY[symbol]

    if issubclass(cls, Actor):
        return cls(x, y, symbol, color, name)
    elif issubclass(cls, Item):
        # Special handling for item subtypes
        if cls == Tool:
            return Tool(x, y, symbol, color, name)
        else:
            return cls(x, y, symbol, color, name)
    else:
        return cls(x, y, symbol, color, name)
