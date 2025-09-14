import colors as COLOR
from constants import PLAYER, PLAYER_NAME
from entities.actor import Actor
from entities.door import Door
from entities.item import Item


class Player(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER, COLOR.DARK_RED, PLAYER_NAME)
        # 玩家库存示例
        self.inventory = {
            "silver_leaf": 5,
            "lemon": 2,
            "glowshroom": 10,
            "moon_dew": 5,
            "glowing_moss": 3,
        }
        self.skills = {
            "Alchemy": 2,
            "Herbalism": 1,
        }
        self.equipped_tool = None
        self.location = "Herb Garden"
        self.tasks = ["Harvest Silver Leaf (3/5)"]

    def get_inventory(self):
        item_list = []
        for item_id, quantity in self.inventory.items():
            item_name = item_id  # TODO: get_item(item_id).name
            item_list.append(f"{item_name} x{quantity}")
        return item_list

    def move(self, dx: int, dy: int, game_map) -> dict[str, bool | str | None]:
        """Move the player if the target position is not blocked"""
        new_x, new_y = self.x + dx, self.y + dy

        # Check for wall collision
        if game_map.is_blocked(new_x, new_y):
            return {"moved": False}

        # Check for entity interaction at new position
        target = None
        for entity in game_map.entities:
            if entity.x == new_x and entity.y == new_y:
                target = entity
                break

        if target:
            if isinstance(target, Door):
                return {"moved": False, "message": target.use(game_map.entities)}
            if isinstance(target, Actor):
                return {"moved": False, "message": self.greet(target)}
            if isinstance(target, Item):
                # Move player first
                self.x, self.y = new_x, new_y
                return {"moved": True, "message": self.pick_up(target, game_map.entities)}
            return {"moved": False}
        self.x, self.y = new_x, new_y
        return {"moved": True}

    def pick_up(self, item, entities):
        """Pick up an item and add it to inventory"""
        if item.name in self.inventory:
            self.inventory[item.name] += 1
        else:
            self.inventory[item.name] = 1
        entities.remove(item)
        return f"Picked up {item.name}"
