"""Text rendering utilities for the game UI"""

from typing import Tuple, Optional
import pygame
from config import COLOR, COLORED_WORDS, WALL, FLOOR


def render_character(surface: pygame.Surface, font: pygame.font.Font, char: str, position: Tuple[int, int], color: Tuple[int, int, int] = COLOR.INK, background: Optional[Tuple[int, int, int]] = None, alpha: Optional[int] = None):
    """Render a single character at the given position"""
    x, y = position
    char_surface = font.render(
        char, False, color, background)
    if alpha and alpha < 255:
        char_surface.set_alpha(alpha)
    surface.blit(char_surface, (x, y))
    return char_surface.get_width()


def render_colored_text(surface: pygame.Surface, font: pygame.font.Font, text: str, position: Tuple[int, int], default_color: Tuple[int, int, int] = COLOR.INK):
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
        word_width = render_character(
            surface, font, word, (x, y), color)

        # Move to next position (add space width)
        x += word_width + get_char_size(font)[0]


def get_char_size(font: pygame.font.Font) -> Tuple[int, int]:
    """Get the width and height of a single character"""
    width, height = font.size(WALL + FLOOR)  # Use a sample character
    return (int(width / 2), height)
