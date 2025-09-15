from typing import List, TYPE_CHECKING
import config.colors as COLOR
from config.symbols import PLAYER, PLAYER_NAME
from entities.actor import Actor
from entities.door import Door
from entities.item import Item
from entities.reference import Reference

if TYPE_CHECKING:
    from world.game_map import GameMap


class Player(Actor):
    """玩家类，继承自Reference但添加了库存等功能"""

    def __init__(self, x: int, y: int):
        super().__init__("player", PLAYER_NAME, x, y,
                         PLAYER, COLOR.DARK_RED, "The player character")
        self.skills = {
            "Alchemy": 2,
            "Herbalism": 1,
        }
        self.equipped_tool = None
        self.location = "Herb Garden"
        self.tasks = ["Harvest Silver Leaf (3/5)"]

    def get_inventory_display(self):
        """获取用于显示的库存列表"""
        return self.inventory.get_display_list()

    def move(self, dx: int, dy: int, game_map: 'GameMap') -> dict[str, bool | str | None]:
        """Move the player if the target position is not blocked"""
        new_x, new_y = self.x + dx, self.y + dy

        # Check for wall collision
        if game_map.is_blocked(new_x, new_y):
            return {"moved": False}

        # Check for entity interaction at new position
        target = None
        for ref in game_map.references:
            if ref.x == new_x and ref.y == new_y:
                target = ref
                break

        if target:
            if isinstance(target, Door):
                # Handle door interaction
                message = target.activate()
                self.x, self.y = new_x, new_y
                return {"moved": True, "message": message}
            if isinstance(target, Actor):
                return {"moved": False, "message": self.greet(target)}
            if isinstance(target, Item):
                # Move player first
                self.x, self.y = new_x, new_y
                return {"moved": True, "message": self.pick_up(target, game_map.references)}
            return {"moved": False}
        self.x, self.y = new_x, new_y
        return {"moved": True}

    def pick_up(self, item: Item, references: List['Reference']):
        """Pick up an item and add it to inventory"""
        self.inventory.add_item(item_id=item.id)
        references.remove(item)
        return f"Picked up {item.name}"
