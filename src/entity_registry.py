import random
from entities import (
    Actor,
    Item,
    Looter,
    Heal,
    Weapon,
    Stairs,
)
import colors as COLOR

ENTITY_REGISTRY = {
    "L": (Looter, COLOR.RED, "Looter", 5, 1),
    "!": (Heal, COLOR.GREEN, "Heal", 0, 0),
    ")": (Weapon, COLOR.INK, "Weapon", 0, 0),
    ">": (Stairs, COLOR.INK, "Stairs", 0, 0),
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
        if cls == Weapon:
            weapons = [("Pipe Wrench", 1), ("Baseball Bat", 2), ("Fire Axe", 3)]
            name, boost = random.choice(weapons)
            return Weapon(x, y, color, name, boost)
        else:
            value = hp  # hp used as value for items
            return cls(x, y, symbol, color, name, value)
    else:
        return cls(x, y, symbol, color, name)
