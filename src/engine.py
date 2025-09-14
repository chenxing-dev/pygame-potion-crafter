"""包含Engine类，处理游戏主循环和渲染"""
from typing import Tuple
import math
import pygame

from config.settings import (
    GAME_TITLE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FONT_SIZE,
    GRID_WIDTH,
    GRID_HEIGHT,
    HEADER_WIDTH,
    HEADER_HEIGHT,
    MENU_WIDTH,
    MENU_HEIGHT,
    MAP_WIDTH,
    MAP_HEIGHT,
    UI_WIDTH,
    UI_HEIGHT,
    INNER_PADDING,
    OUTER_PADDING,
)
from config.symbols import WALL, FLOOR, PLAYER
from entities import Actor, Player
import config.colors as COLOR
from ui import MessageLog, InteractionSystem
from world import GameMap
from crafting.recipe_manager import RecipeManager
from data.recipes import load_recipes


class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        # Create fonts
        self.font = pygame.font.Font(
            "assets/fonts/FT88-Gothique.ttf", FONT_SIZE)

        # Calculate the size of a character
        width, height = self.font.size(WALL + FLOOR)
        self.char_size = (width / 2, height)

        self.game_map: GameMap | None = None  # Will be set in main
        self.player: Player | None = None  # Will be set in main
        # Will be initialized after player and map are set
        self.interaction_system: InteractionSystem | None = None
        self.recipe_manager = RecipeManager()
        load_recipes(self.recipe_manager)

        self.message_log = MessageLog(
            font=self.font, char_size=self.char_size
        )

        # Create container surface
        container_width = GRID_WIDTH * self.char_size[0]
        container_height = GRID_HEIGHT * self.char_size[1]
        container = pygame.Surface(
            (container_width, container_height), pygame.SRCALPHA
        )
        padding_container = pygame.Surface(
            (SCREEN_WIDTH - OUTER_PADDING * 2, SCREEN_HEIGHT - OUTER_PADDING * 2),
            pygame.SRCALPHA,
        )
        self.surfaces = {
            "container": container,
            "padding_container": padding_container
        }

        self.day = 4

    def add_message(self, message, color=COLOR.INK):
        self.message_log.add_message(message, color)

    def render_colored_text(self, surface, text, position, default_color=COLOR.INK):
        self.message_log.render_colored_text(
            surface, text, position, default_color)

    def render(self, game_map, player):
        """Render the game"""

        # Clear container
        self.surfaces["container"].fill(COLOR.PARCHMENT)

        self.render_header()

        self.render_map(game_map, player)

        # Draw UI panel
        self.render_status_panel(player)

        # Draw message log
        self.message_log.render(self.surfaces["container"])

        # Render action menu based on context
        self.render_action_menu()

        # Draw container to screen with padding
        self.surfaces["padding_container"].fill(COLOR.PARCHMENT)
        self.surfaces["padding_container"].blit(
            self.surfaces["container"], (INNER_PADDING, INNER_PADDING))
        self.screen.fill(COLOR.INK)
        self.screen.blit(self.surfaces["padding_container"],
                         (OUTER_PADDING, OUTER_PADDING))

        pygame.display.flip()

    def render_header(self):
        """Render the top title section"""
        # Draw container
        header_x, header_y = 0, 0
        header_bg = pygame.Surface(
            (HEADER_WIDTH * self.char_size[0],
             HEADER_HEIGHT * self.char_size[1]),
            pygame.SRCALPHA,
        )
        # Display game title and current day
        self.render_colored_text(
            header_bg, f"{GAME_TITLE} - Day {self.day}", (0, 0))

        self.surfaces["container"].blit(header_bg, (header_x, header_y))

    def render_map(self, game_map, player):
        """Render the game map and entities"""
        map_x, map_y = 0, self.char_size[1]
        map_bg = pygame.Surface(
            (MAP_WIDTH * self.char_size[0], MAP_HEIGHT * self.char_size[1]),
            pygame.SRCALPHA,
        )

        # Draw tiles
        for x in range(game_map.width):
            for y in range(game_map.height):
                # Get the character and color for this tile
                char = game_map.tiles[x, y]
                color = COLOR.LIGHT_TAUPE if char == FLOOR else COLOR.INK

                # Render the tile character
                text_surface = self.font.render(char, True, color)
                map_bg.blit(
                    text_surface,
                    (x * self.char_size[0], y * self.char_size[1]),
                )

        # Draw entities

        # Create a set of positions occupied by blocking entities
        blocking_positions = set()
        for entity in game_map.entities:
            if entity.blocks and entity != player:
                blocking_positions.add((entity.x, entity.y))

        # Draw non-blocking entities only if not covered by blocking entities
        for entity in game_map.entities:
            if not entity.blocks and entity != player:
                if (entity.x, entity.y) not in blocking_positions:
                    text = self.font.render(
                        entity.char, True, entity.color)
                    map_bg.blit(
                        text,
                        (
                            entity.x * self.char_size[0],
                            entity.y * self.char_size[1],
                        ),
                    )

        # Second: Draw blocking entities (creatures)
        for entity in game_map.entities:
            if entity.blocks and entity != player:

                # Draw creatures
                color = entity.color

                text = self.font.render(entity.char, True, color)
                map_bg.blit(
                    text,
                    (
                        entity.x * self.char_size[0],
                        entity.y * self.char_size[1],
                    ),
                )

        # Third: Draw player (always on top)
        player_text = self.font.render(PLAYER, True, player.color)
        map_bg.blit(
            player_text,
            (
                player.x * self.char_size[0],
                player.y * self.char_size[1],
            ),
        )

        self.surfaces["container"].blit(map_bg, (map_x, map_y))

    def render_status_panel(self, player):
        """Render the status panel"""
        # Draw UI panel background
        ui_x, ui_y = MAP_WIDTH * self.char_size[0], self.char_size[1]
        ui_bg = pygame.Surface(
            (UI_WIDTH * self.char_size[0], UI_HEIGHT * self.char_size[1]),
            pygame.SRCALPHA,
        )

        # Player stats
        status_y = 0
        status = [
            "Location: ",
            (player.location, COLOR.DARK_GREEN),
            "",
            "Task:",
            (player.tasks[0], COLOR.DARK_GREEN),
            "",
            "Inventory:",
            *player.get_inventory(),
        ]

        # Draw stats with colored keywords
        for stat in status:
            if isinstance(stat, Tuple):
                self.render_colored_text(
                    ui_bg,
                    stat[0],
                    (self.char_size[0], status_y),
                    stat[1],
                )
            else:
                self.render_colored_text(
                    ui_bg, stat, (self.char_size[0], status_y))
            status_y += self.char_size[1]

        self.surfaces["container"].blit(ui_bg, (ui_x, ui_y))

    def get_available_actions(self):
        """Determine available actions based on context"""
        # Default actions
        actions = [("L", "ook"), ("I", "nventory")]
        if not self.interaction_system:
            return actions

        if self.interaction_system.interaction_mode:
            return self.interaction_system.get_interaction_menu_items()

        # Add context-sensitive actions
        available_interactions = self.interaction_system.get_available_interactions()
        for action, key in available_interactions:
            actions.insert(0, (key, action[1:]))

        return actions

    def render_action_menu(self):
        """Render the action menu"""

        actions = self.get_available_actions()
        if not actions:
            return
        separator = "|"

        # 绘制动作菜单
        menu_x, menu_y = 0, (GRID_HEIGHT - MENU_HEIGHT) * self.char_size[1]
        current_x = menu_x

        menu_bg = pygame.Surface(
            (MENU_WIDTH * self.char_size[0], MENU_HEIGHT * self.char_size[1]),
            pygame.SRCALPHA,
        )

        for i, action in enumerate(actions):
            # 提取键和文本
            key = f"({action[0]})"
            text = action[1]

            # 绘制首字母（深绿色）
            self.render_colored_text(
                menu_bg, key, (current_x, 0), COLOR.SADDLE_BROWN
            )
            current_x += len(key) * self.char_size[0]

            # 绘制剩余文本（浅灰褐色）
            self.render_colored_text(
                menu_bg, text, (current_x, 0), COLOR.LIGHT_TAUPE
            )
            current_x += (len(text) + 1) * self.char_size[0]

            # 如果不是最后一个动作，添加分隔符
            if i < len(actions) - 1:
                self.render_colored_text(
                    menu_bg, separator, (current_x, 0), COLOR.LIGHT_TAUPE
                )
            current_x += (len(separator) + 1) * self.char_size[0]

        self.surfaces["container"].blit(menu_bg, (menu_x, menu_y))

    def handle_events(self, player: Player, game_map):
        """Handle user input events"""
        keep_running = True

        # Map keys to movement deltas
        move_keys = {
            pygame.K_UP: (0, -1),
            pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_s: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_d: (1, 0),
        }

        for event in pygame.event.get():
            # Handle quit event first
            if event.type == pygame.QUIT:
                keep_running = False
                break

            if event.type != pygame.KEYDOWN:
                continue

            # 优先处理ESCAPE键
            if event.key == pygame.K_ESCAPE:
                keep_running = False
                break

            # 检查消息日志滚动
            if self.message_log.handle_input(event.key):
                continue

            # 如果在交互模式下，让交互系统处理输入
            if self.interaction_system and self.interaction_system.interaction_mode:
                handled = self.interaction_system.handle_interaction_input(
                    event.key)
                if handled:
                    # If interaction input was handled, skip further processing
                    continue

            turn_passed = False

            # Movement keys
            if event.key in move_keys:
                dx, dy = move_keys[event.key]
                result = player.move(dx, dy, game_map)
                if result:  # Either moved or interacted
                    turn_passed = True
                    message = result.get("message")
                    if isinstance(message, Tuple):
                        self.add_message(*message)
                    elif isinstance(message, str):
                        self.add_message(message)

            elif event.key == pygame.K_i:
                # Opening inventory does not pass a turn
                self.show_inventory(player)
                continue

            elif event.key == pygame.K_l:  # 查看
                self.look_around()
                continue

            elif self.interaction_system:
                # Check for context-sensitive actions
                available_interactions = self.interaction_system.get_available_interactions()

                for action_type, key in available_interactions:
                    if event.key == pygame.key.key_code(key):
                        self.interaction_system.start_interaction(action_type)
                        break

            # After handling a player action that passes a turn,
            # advance the world state
            if turn_passed:
                game_map.compute_fov(player.x, player.y)
                self.handle_world_turns(player, game_map)

            # Process only the first handled keydown event
            break

        return keep_running

    def look_around(self):
        """Player looks around and gets descriptions of the surroundings"""
        description = "You look around and see nothing special."
        self.add_message(description)

    def show_inventory(self, player: Player):
        """Display inventory and allow item usage"""
        if not player.inventory:
            self.add_message("Your inventory is empty.")
            return

        self.add_message("Inventory:")
        for _, item in enumerate(player.inventory):
            self.add_message(item)

        # For now, just show the items
        # Later, let the player select one to use

    def handle_world_turns(self, player, game_map):
        """Process world turns after player moves"""
        messages = []

        for entity in game_map.entities[
            :
        ]:  # Use slice copy to avoid modification issues
            if isinstance(entity, Actor) and entity is not player:
                # Calculate distance to player
                distance = math.sqrt(
                    (entity.x - player.x) ** 2 + (entity.y - player.y) ** 2
                )

                if distance <= 8:  # Detection range
                    if distance <= 1:  # Check if player is adjacent
                        # Greets player
                        result = entity.greet(player)
                        messages.append(result)
                    else:
                        # Move toward player using pathfinding
                        new_x, new_y = game_map.find_path(
                            entity.x, entity.y, player.x, player.y, game_map.entities
                        )

                        # Only move if not blocked
                        if not game_map.is_blocked(new_x, new_y):
                            # Check if position is occupied
                            occupied = False
                            for other in game_map.entities:
                                if (
                                    other.blocks
                                    and other != entity
                                    and other.x == new_x
                                    and other.y == new_y
                                ):
                                    occupied = True
                                    break

                            if not occupied:
                                entity.x, entity.y = new_x, new_y

        # Add messages to log
        for msg, color in messages:
            self.add_message(msg, color)

    def move_toward(self, entity, target_x, target_y, game_map):
        # Directions: 4-way
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        # We'll try to minimize the distance to target
        best_dist = float("inf")
        best_move = (entity.x, entity.y)
        for dx, dy in directions:
            nx, ny = entity.x + dx, entity.y + dy
            if not (0 <= nx < game_map.width and 0 <= ny < game_map.height):
                continue
            if game_map.is_blocked(nx, ny):
                continue
            # Check if there's an actor in that position
            occupied = False
            for e in game_map.entities:
                if e.blocks and e.x == nx and e.y == ny:
                    occupied = True
                    break
            if occupied:
                continue

            dist = (nx - target_x) ** 2 + (ny - target_y) ** 2
            if dist < best_dist:
                best_dist = dist
                best_move = (nx, ny)

        # Move the entity
        entity.x, entity.y = best_move
