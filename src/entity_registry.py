from entities import Activator, Actor, Item, Tool, Door
import colors as COLOR


def create_brewing_tower(x, y, char, color, name):
    def examine_callback(_, __):
        return "The main brewing tower is clogged with a dark substance.\n" + \
               "It looks like it needs to be cleaned out before it can be used."

    def clean_callback(_, game):
        player = game.player
        if "Cleaning Gloop" in player.get_inventory():
            game.add_message(
                "You apply the cleaning gloop to the pipes.\n" +
                "It begins dissolving the blockage.", COLOR.DARK_GREEN)
            # Additional logic to mark the brewing tower as cleaned
            return "The pipes begin to gurgle as the blockage is cleared."
        else:
            return "You need a cleaning solution to clear these pipes."

    actions = {
        "Examine": examine_callback,
        "Clean": clean_callback
    }

    return Activator(x, y, char, color, name, actions)


ENTITY_REGISTRY = {
    ")": (Tool, COLOR.DARK_GREEN, "Hammer", None),
    "B": (Activator, COLOR.DARK_RED, "Brewing Tower", create_brewing_tower),
    "+": (Door, COLOR.SADDLE_BROWN, "Door", None),
}


# Generic entity classes
def create_entity(symbol, x, y):
    if symbol not in ENTITY_REGISTRY:
        return None

    cls, color, name, create_func = ENTITY_REGISTRY[symbol]

    if issubclass(cls, Activator):
        return create_func(x, y, symbol, color, name)
    if issubclass(cls, Actor):
        return cls(x, y, symbol, color, name)
    if issubclass(cls, Item):
        # Special handling for item subtypes
        if cls == Tool:
            return Tool(x, y, symbol, color, name)
        return cls(x, y, symbol, color, name)
    return cls(x, y, symbol, color, name)
