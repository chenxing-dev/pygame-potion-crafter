from constants import PLAYER
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
    def __init__(self, x, y, char, color, name, hp, damage):
        super().__init__(x, y, char, color, name, blocks=True)
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.alive = True
        self.armor = 0

    def take_damage(self, amount):
        # Apply armor reduction
        actual_damage = max(0, amount - self.armor)

        self.hp -= actual_damage
        if self.hp <= 0:
            self.alive = False
            return f"{self.name} dies!"
        return f"{self.name} takes {actual_damage} damage!"

    def attack(self, target):
        """Attack another actor and return result message"""
        damage = self.damage
        result = target.take_damage(damage)
        return f"{self.name} {self.get_attack_verb()} you! {result}"

    def get_attack_verb(self):
        """Get appropriate attack verb for this entity type"""
        if isinstance(self, Looter):
            return "stabs"
        elif isinstance(self, Thug):
            return "slams"
        elif isinstance(self, CorruptCop):
            return "shoots"
        return "attacks"


class Player(Actor):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER, COLOR.BLUE, "Sister Evangeline", hp=10, damage=1)
        self.inventory = [("Silver Leaf", 3), ("Lemon Fruit", 2), ("Simple Glue", 1)]
        self.coins = 0
        self.level = 1
        self.xp = 0
        self.current_floor = 1
        self.equipped_weapon = None
        self.location = "Herb Garden"
        self.tasks = ["Harvest Silver Leaf (3/5)"]

    def get_inventory(self):
        return [
            item_stack[0] + (f" x{item_stack[1]}" if item_stack[1] != 1 else "")
            for item_stack in self.inventory
        ]

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
            if isinstance(target, Stairs):  # Check stairs first!
                return self.use_stairs()
            elif isinstance(target, Actor):
                return self.attack(target)
            elif isinstance(target, Item):
                # Move player first
                self.x, self.y = new_x, new_y
                return self.pick_up(target, game_map.entities)
        else:
            self.x, self.y = new_x, new_y
            return True

    def attack(self, target):
        damage = self.damage

        # Calculate damage with equipped weapon
        if self.equipped_weapon:
            damage += self.equipped_weapon.damage_boost

        result = target.take_damage(damage)
        return f"You attack {target.name}! {result}"

    def take_damage(self, amount):
        # Apply armor reduction
        actual_damage = max(0, amount - self.armor)

        self.hp -= actual_damage
        if self.hp <= 0:
            self.alive = False
            return ""
        return f"You take {actual_damage} damage!"

    def pick_up(self, item, entities):
        self.inventory.append(item)
        entities.remove(item)
        return f"Picked up {item.name}"

    def use_stairs(self):
        self.current_floor += 1
        return (
            f"Level {self.current_floor-1} complete! Descending to level {self.current_floor}...",
        )

    def use_item(self, item):
        if isinstance(item, Heal):
            self.hp = min(self.max_hp, self.hp + item.value)
            return f"Used first-aid kit (+{item.value} HP)"
        elif isinstance(item, Weapon):
            self.equipped_weapon = item
            return f"Equipped {item.name} (+{item.damage_boost} DMG)"
        return None


class Looter(Actor):
    pass


class Thug(Actor):
    pass


class CorruptCop(Actor):
    def __init__(self, x, y, symbol, color, name, hp, damage):
        super().__init__(x, y, symbol, color, name, hp, damage)
        self.armor = 1  # Reduced damage taken


class Stairs(Entity):
    def __init__(self, x, y, symbol, color, name):
        super().__init__(x, y, symbol, color, name, blocks=False)


class Item(Entity):
    def __init__(self, x, y, char, color, name, value=0):
        super().__init__(x, y, char, color, name, blocks=False)
        self.value = value


class Heal(Item):
    def __init__(self, x, y, symbol, color, name, value):
        super().__init__(x, y, symbol, color, name, value)


class Weapon(Item):
    def __init__(self, x, y, color, name, damage_boost):
        super().__init__(x, y, ")", color, name, damage_boost)
        self.damage_boost = damage_boost
