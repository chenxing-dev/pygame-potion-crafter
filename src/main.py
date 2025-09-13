# pylint:disable=
import pygame
from engine import Engine
from entities import Player
from map_gen import GameMap

# from constants import GAME_TITLE


def main():
    # Initialize game engine
    engine = Engine()

    # Create game map
    game_map = GameMap()
    game_map.generate_map()

    # Create player at the starting position found in the map
    player = Player(*game_map.player_start)

    # Add starting messages
    engine.add_message("> You are in the Herb Garden. ")
    engine.add_message("> The plants are lush but overgrown. ")
    engine.add_message(
        "> You see a particularly vibrant Silver Leaf ready for harvest. "
    )
    engine.add_message(
        "> A faint glow catches your eye from a patch of moss in the corner. "
    )

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
