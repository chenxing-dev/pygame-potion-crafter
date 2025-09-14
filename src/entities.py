from typing import Callable
from constants import PLAYER, PLAYER_NAME
import colors as COLOR


class Entity:
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks


class Actor(Entity):
    def __init__(self, x, y, char, color, name):
        super().__init__(x, y, char, color, name, blocks=True)
        self.alive = True

    def greet(self, target):
        """Greet another actor and return result message"""
        return f"{self.name} greets {target.name}!"


class Player(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER, COLOR.DARK_RED, PLAYER_NAME)
        self.inventory: list[Item] = (
            []
        )  # ("Silver Leaf", 3), ("Lemon Fruit", 2), ("Simple Glue", 1)
        self.xp = 0
        self.equipped_tool = None
        self.location = "Herb Garden"
        self.tasks = ["Harvest Silver Leaf (3/5)"]

    def get_inventory(self):
        return [item_stack.name for item_stack in self.inventory]

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
        self.inventory.append(item)
        entities.remove(item)
        return f"Picked up {item.name}"


class Item(Entity):
    def __init__(self, x, y, char, color, name):
        super().__init__(x, y, char, color, name, blocks=False)


class Tool(Item):
    pass


class Door(Entity):
    def __init__(self, x, y, char, color, name):
        super().__init__(x, y, char, color, name)

    def use(self, entities):
        entities.remove(self)
        return f"{PLAYER_NAME} opens the door."


class Activator(Entity):
    def __init__(self, x, y, char, color, name, actions: dict[str, Callable]):
        super().__init__(x, y, char, color, name)
        self.actions = actions

    def get_actions(self):
        return list(self.actions.keys())

    def activate(self, action_name: str, game):
        action = self.actions.get(action_name)
        if action:
            return action(self, game)
        return None
