from entities import Activator, Actor, Item, Tool, Door
import config.colors as COLOR


def create_brewing_tower(e_id, x, y, char, color, name):
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
        return "You need a cleaning solution to clear these pipes."

    actions = {
        "examine": examine_callback,
        "clean": clean_callback
    }

    return Activator(e_id, x, y, char, color, name, actions)


ENTITY_REGISTRY = {
    ")": (Tool, COLOR.DARK_GREEN, "hammer", "Hammer", None),
    "B": (Activator, COLOR.DARK_RED, "brewing_tower", "Brewing Tower", create_brewing_tower),
    "+": (Door, COLOR.SADDLE_BROWN, "door", "Door", None),
}


# Generic entity classes
def create_entity(symbol, x, y):
    if symbol not in ENTITY_REGISTRY:
        return None

    cls, color, e_id, name, create_func = ENTITY_REGISTRY[symbol]

    if issubclass(cls, Activator):
        return create_func(e_id, x, y, symbol, color, name)
    if issubclass(cls, Actor):
        return cls(e_id, x, y, symbol, color, name)
    if issubclass(cls, Item):
        # Special handling for item subtypes
        if cls == Tool:
            return Tool(e_id, x, y, symbol, color, name)
        return cls(e_id, x, y, symbol, color, name)
    return cls(e_id, x, y, symbol, color, name)
