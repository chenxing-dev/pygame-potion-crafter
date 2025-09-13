from typing import Tuple
import math
import pygame

from constants import (
    GAME_TITLE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FONT_SIZE,
    WALL,
    FLOOR,
    PLAYER,
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
    MSG_WIDTH,
    MSG_HEIGHT,
    INNER_PADDING,
    OUTER_PADDING,
    COLORED_WORDS,
)
from entities import Actor, Player
import colors as COLOR


class MessageLog:
    def __init__(self, font, char_size):
        self.font = font
        self.char_width, self.char_height = char_size
        # Initialize empty game messages
        self.messages = []
        self.max_lines = MSG_HEIGHT * 3

    def render_colored_text(self, surface, text, position, default_color=COLOR.INK):
        """Render text with colored keywords"""
        x, y = position
        words = text.split()

        for word in words:
            # Check if word needs special coloring
            color = COLORED_WORDS.get(word, default_color)

            if not color:
                # Handle punctuation
                clean_word = word.strip(".,!?;:")
                color = COLORED_WORDS.get(clean_word, default_color)
            # Render the word
            word_surface = self.font.render(word, True, color)
            word_width = word_surface.get_width()

            # Draw the word
            surface.blit(word_surface, (x, y))

            # Move to next position
            x += word_width + self.font.size(" ")[0]  # Add space width

    def add_message(self, message, color=COLOR.INK):
        """Add a message to the log with wrapping and coloring"""

        if message == "":
            self.messages.append(("", color))
            return

        # Split long messages into chunks that fit in the message area
        max_chars = GRID_WIDTH  # Max characters per line
        words = message.split()
        lines = []
        current_line = ""

        for word in words:
            if current_line:
                # If line not empty, we need to add a space before the word
                test_line = current_line + " " + word
            else:
                # First word in line, no space needed
                test_line = word

            # Check if adding this word would exceed the line length
            if len(test_line) <= max_chars:
                current_line = test_line
            else:
                # Word doesn't fit - finish current line and start new one
                if current_line:  # Only add if not empty
                    lines.append(current_line)
                current_line = word

                # Handle words longer than max_chars
                while len(current_line) > max_chars:
                    # Split the oversized word
                    lines.append(current_line[:max_chars])
                    current_line = current_line[max_chars:]

        # Add the last line
        if current_line:
            lines.append(current_line)

        # Add all lines to message log
        for line in lines:
            self.messages.append((line, color))

        # Keep message log manageable
        if len(self.messages) > self.max_lines:
            self.messages = self.messages[-self.max_lines:]

    def render(self, container):
        """Render messages with colored keywords"""
        msg_x, msg_y = 0, (HEADER_HEIGHT + MAP_HEIGHT) * self.char_height

        # Draw message log background
        msg_bg = pygame.Surface(
            (MSG_WIDTH * self.char_width, MSG_HEIGHT * self.char_height),
            pygame.SRCALPHA,
        )

        # Draw messages
        for i, (msg, color) in enumerate(self.messages[-MSG_HEIGHT:]):
            self.render_colored_text(
                msg_bg,
                msg,
                (0, i * self.char_height),
                color,
            )

        container.blit(msg_bg, (msg_x, msg_y))


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
        actions = self.get_available_actions()
        self.render_action_menu(actions)

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
            if entity.blocks and entity != player and entity.alive:
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
            if entity.blocks and entity != player and entity.alive:

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
        if player.alive:
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
        # For simplicity, return a static list for now
        return ["Examine", "Harvest", "Look", "Inventory", "Map"]

    def render_action_menu(self, actions):
        """Render the action menu"""
        separator = "|"

        # 绘制动作菜单
        menu_x, menu_y = 0, (GRID_HEIGHT - MENU_HEIGHT) * self.char_size[1]
        current_x = 0

        menu_bg = pygame.Surface(
            (MENU_WIDTH * self.char_size[0], MENU_HEIGHT * self.char_size[1]),
            pygame.SRCALPHA,
        )

        for i, action in enumerate(actions):
            # 提取首字母和剩余部分
            first_letter = f"({action[0]})"
            rest_of_text = action[1:]

            # 绘制首字母（深绿色）
            self.render_colored_text(
                menu_bg, first_letter, (current_x, 0), COLOR.SADDLE_BROWN
            )
            current_x += len(first_letter) * self.char_size[0]

            # 绘制剩余文本（浅灰褐色）
            self.render_colored_text(
                menu_bg, rest_of_text, (current_x, 0), COLOR.LIGHT_TAUPE
            )
            current_x += (len(rest_of_text) + 1) * self.char_size[0]

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
            if event.type == pygame.QUIT:
                keep_running = False
                break

            if event.type != pygame.KEYDOWN:
                continue

            # Global quit
            if event.key == pygame.K_ESCAPE:
                keep_running = False
                break

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

            elif event.key == pygame.K_e:
                # Examine action
                self.add_message("You examine your surroundings.")

            elif event.key == pygame.K_i:
                # Opening inventory does not pass a turn
                self.show_inventory(player)
                continue

            # After handling a player action that passes a turn,
            # advance the world state
            if turn_passed and player.alive:
                game_map.compute_fov(player.x, player.y)
                self.handle_world_turns(player, game_map)

            # Process only the first handled keydown event
            break

        return keep_running

    def show_inventory(self, player):
        """Display inventory and allow item usage"""
        if not player.inventory:
            self.add_message("Your inventory is empty.")
            return

        self.add_message("Inventory:")
        for _, item in enumerate(player.inventory):
            self.add_message(item.name)

        # For now, just show the items
        # Later, let the player select one to use

    def handle_world_turns(self, player, game_map):
        """Process world turns after player moves"""
        messages = []

        for entity in game_map.entities[
            :
        ]:  # Use slice copy to avoid modification issues
            if isinstance(entity, Actor) and entity is not player and entity.alive:
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
                if e.blocks and e.x == nx and e.y == ny and e.alive:
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
