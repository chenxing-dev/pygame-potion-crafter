"""主游戏循环与状态管理"""
from enum import Enum, auto
from typing import Optional, Tuple
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
    UI_WIDTH,
    UI_HEIGHT,
    INNER_PADDING,
    OUTER_PADDING,
)
from config import COLOR, WALL, FLOOR
from data.object_manager import object_manager
from crafting import RecipeManager
from entities import Door, MobilePlayer, NPC, Player, Reference
from ui import MessageLog, InteractionSystem
from world import GameMap, MAP_DATA


class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    INVENTORY = auto()
    CRAFTING = auto()
    JOURNAL = auto()


class Game:
    def __init__(self):
        # 初始化 pygame 与主窗口
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game states
        self.state = GameState.MAIN_MENU
        self.previous_state: Optional[GameState] = None

        # 字体与字符尺寸
        self.font = pygame.font.Font(
            "assets/fonts/FT88-Gothique.ttf", FONT_SIZE)
        width, height = self.font.size(WALL + FLOOR)
        self.char_size = (int(width / 2), height)

        # 渲染用 surface 容器
        container_w = GRID_WIDTH * self.char_size[0]
        container_h = GRID_HEIGHT * self.char_size[1]
        self.surfaces = {}
        self.surfaces["container"] = pygame.Surface(
            (container_w, container_h)).convert()
        pad_w, pad_h = container_w + 2 * INNER_PADDING, container_h + 2 * INNER_PADDING
        self.surfaces["padding_container"] = pygame.Surface(
            (pad_w, pad_h), pygame.SRCALPHA).convert_alpha()

        # 初始化对象管理器
        self.object_manager = object_manager

        # 游戏组件（将在 main 中设置）
        self.player: Optional[Reference[Player]] = None
        self.mobile_player: Optional[MobilePlayer] = None
        self.world: Optional[GameMap] = None
        self.world_state: dict = {"day": 1, "tasks": []}
        self.recipe_manager = None
        self.journal = None
        self.message_log = MessageLog(font=self.font, char_size=self.char_size)
        self.interaction_system: Optional[InteractionSystem] = None

        # Sample map
        self.map_data = str(MAP_DATA.strip()).splitlines()

    def initialize_game(self):
        """初始化所有游戏组件"""
        # 1. 添加对象到游戏中 first
        self.add_objects_to_game()

        # 2. Initialize the game map
        self.world = GameMap(self.map_data)

        # 2. Initialize the player at the starting position found in the map
        self.create_player(*self.world.player_start)
        if self.player and self.world:
            self.world.compute_fov(self.player.x, self.player.y)

        # 3. 初始化其他系统
        self.recipe_manager = RecipeManager()
        self.interaction_system = InteractionSystem(self)
        self.world_state["tasks"] = ["Harvest Silver Leaf (3/5)"]  # TODO: 临时任务

        # 4. Add starting messages
        self.add_message(
            "> You enter the quiet workshop. Dust motes dance in the sunlight."
        )
        self.add_message(
            "> The main brewing station stands silent, its pipes clogged with dark residue.",
            COLOR.DARK_RED,
        )

        # 初始化玩家库存
        self.add_item("silver_leaf", 5)
        self.add_item("lemon", 2)
        self.add_item("glowshroom", 10)
        self.add_item("moon_dew", 5)
        self.add_item("glowing_moss", 3)

    def create_reference(self, entity, x: int, y: int) -> Reference:
        """创建实体引用"""
        if self.world is None:
            raise ValueError(
                "World must be initialized before creating references.")
        reference = Reference(x, y, entity)
        self.world.references.append(reference)
        return reference

    def create_player(self, x: int, y: int):
        """创建玩家实体并返回其引用"""
        player_entity = Player()
        self.player = self.create_reference(player_entity, x, y)
        self.mobile_player = MobilePlayer(x, y, self.player)

    def add_item(self, item_id: str, quantity: int = 1):
        """向玩家库存添加物品"""
        if self.player:
            self.player.object_data.inventory.add_item(item_id, quantity)

    def add_objects_to_game(self):
        """向游戏添加对象"""
        self.object_manager.add_object(
            Door(door_id="door", name="Door"))
        print(
            f"Objects in manager: {list(self.object_manager.objects.keys())}")

    def change_state(self, new_state):
        """Change the current game state"""
        self.previous_state = self.state
        self.state = new_state

    def add_message(self, message, color=COLOR.INK):
        self.message_log.add_message(message, color)

    def render_colored_text(self, surface, text, position, default_color=COLOR.INK):
        self.message_log.render_colored_text(
            surface, text, position, default_color)

    def render(self):
        """Render the game"""
        # Clear container
        self.surfaces["container"].fill(COLOR.PARCHMENT)

        if self.state == GameState.MAIN_MENU:
            self.render_main_menu()
        elif self.state == GameState.PLAYING:
            self.render_playing()
        elif self.state == GameState.INVENTORY:
            self.render_inventory()
        elif self.state == GameState.CRAFTING:
            self.render_crafting()
        elif self.state == GameState.JOURNAL:
            self.render_journal()

        # Compose framed container and blit to the screen
        self.draw_framed_container()
        pygame.display.flip()

    def draw_framed_container(self):
        """Draw a framed container with padding"""
        # Draw inner parchment area
        self.surfaces["padding_container"].fill(COLOR.PARCHMENT)
        self.surfaces["padding_container"].blit(
            self.surfaces["container"], (INNER_PADDING, INNER_PADDING))
        # Fill frame
        self.screen.fill(COLOR.INK)
        self.screen.blit(self.surfaces["padding_container"],
                         (OUTER_PADDING, OUTER_PADDING))

    def render_main_menu(self):
        """Render the main menu"""
        # Draw container
        main_menu_x, main_menu_y = 0, 0
        main_menu_bg = pygame.Surface(
            (GRID_WIDTH * self.char_size[0],
             GRID_HEIGHT * self.char_size[1]),
            pygame.SRCALPHA,
        )
        # Display game title and instructions
        self.render_colored_text(
            main_menu_bg, GAME_TITLE, (0, 0))
        self.render_colored_text(
            main_menu_bg, "Press ENTER to begin", (0, self.char_size[1]))
        self.surfaces["container"].blit(
            main_menu_bg, (main_menu_x, main_menu_y))

    def render_playing(self):
        """Render the playing state"""
        # Render game world
        if self.world and self.player:
            self.world.render(
                self.surfaces["container"],
                self.char_size,
                self.font
            )

        # Render UI elements
        self.render_ui_panel()

    def render_inventory(self):
        """Render the inventory screen"""
        self.render_header()
        # TODO: Render inventory items

    def render_crafting(self):
        """Render the crafting screen"""
        self.render_header()
        # TODO: Render crafting items

    def render_journal(self):
        """Render the journal screen"""
        self.render_header()
        # TODO: Render journal entries

    def render_ui_panel(self):
        """Render the UI panel for the playing state"""
        self.render_header()
        self.render_status_panel()
        self.message_log.render(self.surfaces["container"])
        self.render_action_menu()

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
            header_bg, f"{GAME_TITLE} - Day {self.world_state['day']}", (0, 0))

        self.surfaces["container"].blit(header_bg, (header_x, header_y))

    def render_status_panel(self):
        """Render the status panel"""
        # Draw UI panel background
        ui_x, ui_y = MAP_WIDTH * self.char_size[0], self.char_size[1]
        ui_bg = pygame.Surface(
            (UI_WIDTH * self.char_size[0], UI_HEIGHT * self.char_size[1]),
            pygame.SRCALPHA,
        )
        if not self.player or not self.mobile_player:
            return
        # Player stats
        status_y = 0
        status = [
            "Location: ",
            (self.mobile_player.location, COLOR.DARK_GREEN),
            "",
            "Task:",
            (self.world_state["tasks"][0], COLOR.DARK_GREEN),
            "",
            "Inventory:",
            *self.player.object_data.get_inventory_display(),
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

    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            # Handle quit event first
            if event.type == pygame.QUIT:
                self.running = False
                break

            if event.type == pygame.KEYDOWN:
                # 优先处理ESCAPE键
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break

            if self.state == GameState.MAIN_MENU:
                self.handle_main_menu_events(event)
            elif self.state == GameState.PLAYING:
                self.handle_playing_events(event)
            elif self.state == GameState.INVENTORY:
                self.handle_inventory_events(event)
            elif self.state == GameState.CRAFTING:
                self.handle_crafting_events(event)
            elif self.state == GameState.JOURNAL:
                self.handle_journal_events(event)

    def handle_main_menu_events(self, event):
        """Handle events for the main menu state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.initialize_game()
                self.change_state(GameState.PLAYING)

    def handle_playing_events(self, event):
        """Handle events during the main gameplay state"""
        if event.type != pygame.KEYDOWN:
            return self.running

        # 检查消息日志滚动
        if self.message_log.handle_input(event.key):
            return

        # 如果在交互模式下，让交互系统处理输入
        if self.interaction_system and self.interaction_system.interaction_mode:
            handled = self.interaction_system.handle_interaction_input(
                event.key)
            if handled:
                # If interaction input was handled, skip further processing
                return

        turn_passed = False

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

        if event.key in move_keys and self.player and self.player.mobile:
            print(f"Movement key pressed: {event.key}")
            dx, dy = move_keys[event.key]
            print(f"Attempting to move by ({dx}, {dy})")
            result = self.player.mobile.move(dx, dy, self)
            print(f"Move result: {result}")
            if result:  # Either moved or interacted
                turn_passed = True
                message = result.get("message")
                if isinstance(message, Tuple):
                    self.add_message(*message)
                elif isinstance(message, str):
                    self.add_message(message)

        elif event.key == pygame.K_i:
            if self.player:
                self.change_state(GameState.INVENTORY)
            return

        elif event.key == pygame.K_j:
            if self.player:
                self.change_state(GameState.JOURNAL)
            return

        elif event.key == pygame.K_l:  # 查看
            self.look_around()
            return

        elif self.interaction_system:
            # Check for context-sensitive actions
            available_interactions = self.interaction_system.get_available_interactions()

            for action_type, key in available_interactions:
                if event.key == pygame.key.key_code(key):
                    self.interaction_system.start_interaction(action_type)
                    break

        # After handling a player action that passes a turn,
        # advance the world state
        if turn_passed and self.world and self.player:
            self.world.compute_fov(self.player.x, self.player.y)
            self.handle_world_turns()

        return self.running

    def handle_crafting_events(self, event):
        """Handle events for the crafting state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                self.change_state(GameState.PLAYING)

    def handle_inventory_events(self, event):
        """Handle events for the inventory state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.change_state(GameState.PLAYING)

    def handle_journal_events(self, event):
        """Handle events for the journal state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                self.change_state(GameState.PLAYING)

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
        self.add_message(player.get_inventory_display())

    def handle_world_turns(self):
        """Process world turns after player moves"""
        if not self.world or not self.player:
            return

        messages = []

        # iterate over a copy to avoid mutation issues
        for ref in list(self.world.references):
            # ensure the referenced object is an NPC and it's not the player reference
            if not isinstance(ref.object_data, NPC) or ref is self.player:
                continue

            # ensure a Mobile exists and narrow its type for the checker
            if not hasattr(ref, "mobile") or ref.mobile is None:
                continue

            # Calculate distance to player
            distance = math.sqrt(
                (ref.x - self.player.x) ** 2 + (ref.y - self.player.y) ** 2
            )

            if distance <= 8:  # Detection range
                if distance <= 1:  # Check if player is adjacent
                    # Greets player
                    result = ref.mobile.greet(self.player)
                    messages.append(result)
                else:
                    # Move toward player using pathfinding
                    new_x, new_y = self.world.find_path(
                        ref.x, ref.y, self.player.x, self.player.y, self.world.references
                    )

                    # Only move if not blocked
                    if not self.world.is_blocked(new_x, new_y):
                        # Check if position is occupied
                        occupied = False
                        for other in self.world.references:
                            if (
                                other.object_data.blocks
                                and other != ref
                                and other.x == new_x
                                and other.y == new_y
                            ):
                                occupied = True
                                break

                        if not occupied:
                            ref.x, ref.y = new_x, new_y

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

    def run(self):
        """Run the main game loop"""
        while self.running:
            # Handle events
            self.handle_events()

            # Render everything
            self.render()

            # Cap at 60 FPS
            self.clock.tick(60)

        pygame.quit()
