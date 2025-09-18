from typing import List, TYPE_CHECKING, cast
import config.colors as COLOR
from config.symbols import PLAYER, PLAYER_NAME
from entities.game_object import ObjectType
from entities.mobile import Mobile
from entities.npc import NPC
from entities.item import Item
from entities.reference import Reference

if TYPE_CHECKING:
    from game import Game


class Player(NPC):
    """玩家类，继承自 NPC"""

    def __init__(self):
        NPC.__init__(self, actor_id="player", name=PLAYER_NAME,
                     char=PLAYER, color=COLOR.DARK_RED)


class MobilePlayer(Mobile):
    """玩家类，继承自 Mobile"""

    def __init__(self, x: int, y: int, reference: 'Reference[Player]'):
        super().__init__(x, y, reference)
        self.object_data: Player = reference.object_data  # 关联的实体对象，如Player
        self.skills = {
            "Alchemy": 2,
            "Herbalism": 1,
        }
        self.equipped_tool = None
        self.location = "Herb Garden"

        # Keep the reference's mobile link
        self.reference.mobile = self

    def move(self, dx: int, dy: int, game: 'Game') -> dict[str, bool | str | None]:
        """Move the player if the target position is not blocked"""
        new_x, new_y = self.x + dx, self.y + dy

        if game.world is None:
            print("Game world is not initialized.")
            return {"moved": False}

        # Check for wall collision
        if game.world.is_blocked(new_x, new_y):
            print(f"Movement blocked at ({new_x}, {new_y})")
            return {"moved": False}

        # Check for entity interaction at new position
        target = None
        for ref in game.world.references:
            if ref.x == new_x and ref.y == new_y:
                # Ignore floor and wall references
                if ref.object_data.interactable:
                    target = ref
                    break

        if target:
            print(f"Interacting with entity {target.id} at ({new_x}, {new_y})")
            if target.object_data.blocks:
                print(f"Entity {target.id} blocks movement.")
                if target.object_data.object_type == ObjectType.DOOR:
                    print("Door interaction")
                    # Handle door interaction
                    message = target.activate(game)
                    super().move(dx, dy, game)
                    return {"moved": True, "message": message}
                if target.object_data.object_type == ObjectType.NPC:
                    return {"moved": False, "message": self.greet(target)}
            else:
                print(f"Entity {target.id} does not block movement.")
                if target.object_data.object_type == ObjectType.ITEM:
                    super().move(dx, dy, game)
                    return {"moved": True, "message": self.pick_up(cast(Reference[Item], target), game.world.references)}
                print(f"Moving onto non-blocking entity at ({new_x}, {new_y})")
                super().move(dx, dy, game)
                game.world.reset_door()

        # No target entity, just move
        super().move(dx, dy, game)
        game.world.reset_door()
        return {"moved": True}

    def pick_up(self, item_ref: 'Reference[Item]', references: List['Reference']):
        """Pick up an item and remove it from the world references"""
        self.reference.object_data.inventory.add_item(
            item_id=item_ref.object_data.id)
        references.remove(item_ref)
        return f"Picked up {item_ref.object_data.name}"
