from typing import List, Tuple, TYPE_CHECKING, Union, cast
import numpy as np
import pygame
from config import COLOR, WALL, FLOOR, PLAYER, MAP_WIDTH, MAP_HEIGHT
from data.object_manager import object_manager
from entities.game_object import ObjectType
from entities.reference import Reference
from entities.activator import Activator
from entities.static import Static
from entities.item import Item
from entities.door import Door

if TYPE_CHECKING:
    from entities.physical_object import PhysicalObject
    from entities.npc import NPC
    from entities.player import Player


class GameMap:
    def __init__(self, map_strings: List[str]):
        self.width, self.height = MAP_WIDTH, MAP_HEIGHT
        self.fov = np.zeros((self.width, self.height), dtype=bool)
        self.explored = np.zeros((self.width, self.height), dtype=bool)

        # Store references here
        self.references: List[Reference['PhysicalObject']] = []
        self.player_start = (3, 3)  # default starting position

        # Load the map from the provided strings
        self.load_from_strings(map_strings)

    def create_reference(self, object_data: 'Union[PhysicalObject, Item, Activator, Static, Player, NPC]', position: Tuple[int, int]):
        """创建Reference并添加到地图"""
        reference = Reference(*position, object_data=object_data)
        self.references.append(reference)
        return reference

    def load_from_strings(self, map_strings: list):
        """从字符串列表加载地图"""
        # Convert text map to grid
        for y, row in enumerate(map_strings):
            for x, char in enumerate(row):
                if self.is_within_bounds(x, y):
                    # Set tile type
                    wall = Static("wall", WALL, COLOR.INK, blocks=True)
                    floor = Static(
                        "floor", FLOOR, COLOR.LIGHT_TAUPE, blocks=False)
                    if char == WALL:
                        self.create_reference(
                            object_data=wall, position=(x, y))
                    elif char == FLOOR:
                        self.create_reference(
                            object_data=floor, position=(x, y))
                    else:
                        self.create_reference(
                            object_data=floor, position=(x, y))

                    # Place entities
                    if char == PLAYER:
                        # This is the player starting position
                        self.player_start = (x, y)
                    elif char == '+':
                        door = object_manager.get_object("door")
                        if isinstance(door, Door):
                            self.create_reference(
                                object_data=door, position=(x, y))

    def get_reference_at(self, x: int, y: int):
        """获取指定位置的参照物"""
        for ref in self.references:
            if ref.x == x and ref.y == y:
                return ref
        return None

    def is_within_bounds(self, x, y):
        """Check if coordinates are within map bounds"""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_blocked(self, x, y):
        """Check if a tile is blocked"""
        # Check tile blocking
        tile = self.get_reference_at(x, y)
        if tile and tile.object_data.blocks:
            return True
        return False

    def is_blocked_by_entity(self, x, y, entities):
        """Check if a position is blocked by an entity"""
        for entity in entities:
            if entity.blocks and entity.x == x and entity.y == y:
                return True
        return False

    def compute_fov(self, player_x, player_y, radius=3):
        # Reset FOV
        self.fov.fill(False)

        # Simple circular FOV
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x = player_x + dx
                y = player_y + dy
                if self.is_within_bounds(x, y):
                    if dx * dx + dy * dy <= radius * radius:
                        self.fov[x, y] = True
                        self.explored[x, y] = True

    def find_path(self, start_x, start_y, target_x, target_y, entities):
        """A* pathfinding algorithm with obstacle avoidance"""

        # Simple heuristic: Manhattan distance
        def heuristic(x1, y1, x2, y2):
            return abs(x1 - x2) + abs(y1 - y2)

        # Possible moves (4 directions)
        directions = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),  # Cardinal directions
        ]

        # Initialize open and closed sets
        open_set = []
        closed_set = set()

        # Add start node
        start_node = (
            start_x,
            start_y,
            0,
            heuristic(start_x, start_y, target_x, target_y),
            None,
        )
        open_set.append(start_node)

        while open_set:
            # Find node with lowest f_score
            current = min(open_set, key=lambda node: node[3])
            open_set.remove(current)
            closed_set.add((current[0], current[1]))

            # Check if we reached target
            if current[0] == target_x and current[1] == target_y:
                # Reconstruct path
                path = []
                while current[4]:  # Follow parent pointers
                    path.append((current[0], current[1]))
                    current = current[4]
                if path:
                    return path[-1]  # Return next step in path
                return (start_x, start_y)  # Stay in place if no path

            # Check neighbors
            for dx, dy in directions:
                nx, ny = current[0] + dx, current[1] + dy

                # Skip if out of bounds or blocked
                if not self.is_within_bounds(nx, ny):
                    continue
                if self.is_blocked(nx, ny):
                    continue

                # Skip if occupied by another blocking entity
                occupied = False
                for entity in entities:
                    if (
                        entity.blocks
                        and entity != self
                        and entity.x == nx
                        and entity.y == ny
                    ):
                        occupied = True
                        break
                if occupied:
                    continue

                # Skip if already in closed set
                if (nx, ny) in closed_set:
                    continue

                # Calculate new g_score (cost from start)
                new_g = current[2] + 1

                # Check if this node is already in open set
                in_open = False
                for node in open_set:
                    if node[0] == nx and node[1] == ny:
                        in_open = True
                        if new_g < node[2]:
                            # Update with better path
                            node = (
                                nx,
                                ny,
                                new_g,
                                new_g + heuristic(nx, ny, target_x, target_y),
                                current,
                            )
                        break

                if not in_open:
                    # Add new node to open set
                    new_node = (
                        nx,
                        ny,
                        new_g,
                        new_g + heuristic(nx, ny, target_x, target_y),
                        current,
                    )
                    open_set.append(new_node)

        # No path found
        return (start_x, start_y)

    def render(self, surface: pygame.Surface, char_size: Tuple[int, int], font: pygame.font.Font):
        """Render the game map and entities"""
        map_x, map_y = 0, char_size[1]
        map_bg = pygame.Surface(
            (MAP_WIDTH * char_size[0], MAP_HEIGHT * char_size[1]),
            pygame.SRCALPHA,
        )

        # Draw references (floor, walls, items, etc.)
        for ref in self.references:
            char = getattr(ref.object_data, "char", None)
            color = getattr(ref.object_data, "color", None)
            if not char or not color:
                continue
            if self.fov[ref.x, ref.y]:
                text_surface = font.render(
                    char, True, color)
                map_bg.blit(
                    text_surface,
                    (ref.x * char_size[0], ref.y * char_size[1]),
                )
            elif self.explored[ref.x, ref.y]:
                dimmed_color = (
                    min(color[0] + (255 - color[0]) // 2, 255),
                    min(color[1] + (255 - color[1]) // 2, 255),
                    min(color[2] + (255 - color[2]) // 2, 255),
                )
                text_surface = font.render(
                    char, True, dimmed_color)
                map_bg.blit(
                    text_surface,
                    (ref.x * char_size[0], ref.y * char_size[1]),
                )

        surface.blit(map_bg, (map_x, map_y))

    def reset_door(self):
        for ref in self.references:
            if ref.object_data.object_type == ObjectType.DOOR:
                ref.object_data = cast('Door', ref.object_data)
                ref.object_data.blocks = True
                ref.object_data.char = ref.object_data.close_char
