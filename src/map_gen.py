import numpy as np
from constants import FLOOR, WALL, PLAYER, MAP_WIDTH, MAP_HEIGHT
from entity_registry import ENTITY_REGISTRY, create_entity


# Sample map
templates = {
    1: [
        "##################################",
        "#................................#",
        "#.....#####......................#",
        "#.....#   #......................#",
        "#.....+   #......................#",
        "#.....#####......................#",
        "#................................#",
        "#................................#",
        "#..........@.....................#",
        "#................................#",
        "#.................#####..........#",
        "#.................#   #..........#",
        "#.................#   #..........#",
        "#.................#####..........#",
        "#................................#",
        "##################################",
    ]
}


class GameMap:
    def __init__(self, level=1):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.tiles = np.full((self.width, self.height), fill_value=FLOOR, dtype=str)
        self.player_start = (3, 3)  # default
        self.level = level
        self.entities = []  # Store entities here

        self.fov = np.zeros((self.width, self.height), dtype=bool)
        self.explored = np.zeros((self.width, self.height), dtype=bool)

    def generate_map(self):
        """Load map from a list of strings"""
        string_array = templates.get(self.level, templates[1])
        self.height = len(string_array)
        self.width = len(string_array[0])
        self.tiles = np.full((self.width, self.height), fill_value=FLOOR, dtype="str")

        self.entities = []  # Reset entities
        self.player_start = (3, 3)  # default

        # Convert text map to grid
        for y, row in enumerate(string_array):
            for x, char in enumerate(row):
                if x < self.width and y < self.height:
                    # Set tile type
                    if char in (WALL, FLOOR):
                        self.tiles[x, y] = char
                    else:
                        self.tiles[x, y] = FLOOR  # Entities on floor tiles

                    # Place entities
                    if char == PLAYER:
                        # This is the player starting position
                        self.player_start = (x, y)
                    elif char in ENTITY_REGISTRY:
                        entity = create_entity(char, x, y)
                        if entity:
                            self.entities.append(entity)

    def is_blocked(self, x, y):
        """Check if a tile is blocked (wall)"""
        return self.tiles[x, y] == WALL

    def is_blocked_by_entity(self, x, y, entities):
        """Check if a position is blocked by an entity"""
        for entity in entities:
            if entity.blocks and entity.x == x and entity.y == y:
                return True
        return False

    def compute_fov(self, player_x, player_y, radius=8):
        # Reset FOV
        self.fov.fill(False)

        # Simple circular FOV
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x = player_x + dx
                y = player_y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
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
                if not (0 <= nx < self.width and 0 <= ny < self.height):
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
