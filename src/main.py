"""游戏入口点，初始化游戏并启动主循环"""
# pylint:disable=
import pygame
from engine import Engine, InteractionSystem
from entities import Player
from world import GameMap
from config import COLOR


def main():
    # Initialize game engine
    engine = Engine()

    # Create game map
    game_map = GameMap()

    # Sample map
    map_data = [
        "##################################",
        "#................................#",
        "#.....#####......................#",
        "#.....#   #......................#",
        "#.....+   #......................#",
        "#.....#####......................#",
        "#..............B.................#",
        "#................................#",
        "#..........@.....................#",
        "#................................#",
        "#.................#####..........#",
        "#.................#   #..........#",
        "#.................#   #..........#",
        "#.................#   #..........#",
        "###################   ############",
    ]
    game_map.load_from_strings(map_data)
    engine.game_map = game_map

    # Create player at the starting position found in the map
    player = Player(*game_map.player_start)
    engine.player = player

    engine.interaction_system = InteractionSystem(engine)

    # Add starting messages
    engine.add_message(
        "> You enter the quiet workshop. Dust motes dance in the sunlight."
    )
    engine.add_message(
        "> The main brewing station stands silent, its pipes clogged with dark residue.",
        COLOR.DARK_RED,
    )

    # 初始化玩家库存
    player.inventory.add_item("silver_leaf", 5)
    player.inventory.add_item("lemon", 2)
    player.inventory.add_item("glowshroom", 10)
    player.inventory.add_item("moon_dew", 5)
    player.inventory.add_item("glowing_moss", 3)

    # Main game loop
    running = True
    while running:
        # Handle events
        running = engine.handle_events(player, game_map)

        # Render everything
        engine.render(game_map, player)

        # Cap at 60 FPS
        engine.clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
