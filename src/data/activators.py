from config import COLOR
from entities.activator import Activator
from entities.door import Door


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


def create_activators(object_manager):
    object_manager.add_object(Door(door_id="door", name="Door"))
    object_manager.add_object(Activator(
        "brewing_station",
        "Brewing Station",
        "B",
        COLOR.DARK_RED,
        {
            "examine": examine_brewing_station,
            "clean": clean_brewing_station
        }
    ))
