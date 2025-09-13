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
        self.armor = 0

    def greet(self, target):
        """Greet another actor and return result message"""
        return f"{self.name} greets {target.name}!"


class Player(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER, COLOR.BLUE, PLAYER_NAME)
        self.inventory = (
            []
        )  # ("Silver Leaf", 3), ("Lemon Fruit", 2), ("Simple Glue", 1)
        self.xp = 0
        self.equipped_tool = None
        self.location = "Herb Garden"
        self.tasks = ["Harvest Silver Leaf (3/5)"]

    def get_inventory(self):
        return [item_stack.name for item_stack in self.inventory]

    def move(self, dx, dy, game_map):
        """Move the player if the target position is not blocked"""
        new_x, new_y = self.x + dx, self.y + dy

        # Check for wall collision
        if game_map.is_blocked(new_x, new_y):
            return None

        # Check for entity interaction at new position
        target = None
        for entity in game_map.entities:
            if entity.x == new_x and entity.y == new_y:
                target = entity
                break

        if target:
            if isinstance(target, Actor):
                return self.greet(target)
            elif isinstance(target, Item):
                # Move player first
                self.x, self.y = new_x, new_y
                return self.pick_up(target, game_map.entities)
        else:
            self.x, self.y = new_x, new_y
            return True

    def pick_up(self, item, entities):
        self.inventory.append(item)
        entities.remove(item)
        return f"Picked up {item.name}"

    def use_item(self, item):
        if isinstance(item, Tool):
            self.equipped_tool = item
            return f"Equipped {item.name}"
        return None


class Item(Entity):
    def __init__(self, x, y, char, color, name, value=0):
        super().__init__(x, y, char, color, name, blocks=False)
        self.value = value


class Tool(Item):
    def __init__(self, x, y, char, color, name):
        super().__init__(x, y, char, color, name)
