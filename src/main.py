# pylint:disable=
import pygame
from engine import Engine
from entities import Player
from map_gen import GameMap
import colors as COLOR


def main():
    # Initialize game engine
    engine = Engine()

    # Create game map
    game_map = GameMap()
    game_map.generate_map()

    # Create player at the starting position found in the map
    player = Player(*game_map.player_start)

    # Add starting messages
    engine.add_message(
        "> You enter the quiet workshop. Dust motes dance in the sunlight."
    )
    engine.add_message(
        "> The main brewing tower stands silent, its pipes clogged with dark residue.",
        COLOR.DARK_RED,
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
