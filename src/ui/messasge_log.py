import pygame
from config import COLOR
from config.settings import GRID_WIDTH, HEADER_HEIGHT, MAP_HEIGHT, MSG_WIDTH, MSG_HEIGHT
from ui.text_renderer import render_colored_text


class MessageLog:
    def __init__(self, font, char_size):
        self.font = font
        self.char_width, self.char_height = char_size
        # Initialize empty game messages
        self.messages = []
        self.max_lines = MSG_HEIGHT * 3
        self.scroll_offset = 0

    def add_message(self, message, color=COLOR.INK):
        """Add a message to the log with wrapping and coloring"""

        if message == "":
            self.messages.append(("", color))
            return

        # 分割消息以适应宽度
        lines = self.split_message(message)

        # Add all lines to message log
        for line in lines:
            self.messages.append((line, color))

        # Keep message log manageable
        if len(self.messages) > self.max_lines:
            self.messages = self.messages[-self.max_lines:]

        # Auto-scroll to bottom
        self.scroll_to_bottom()

    def split_message(self, message):
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

        return lines

    def scroll_to_bottom(self):
        """Scroll to the bottom of the message log"""
        self.scroll_offset = max(0, len(self.messages) - MSG_HEIGHT)

    def scroll_up(self):
        """Scroll up one line"""
        self.scroll_offset = max(0, self.scroll_offset - 1)

    def scroll_down(self):
        """Scroll down one line"""
        self.scroll_offset = min(len(self.messages) - MSG_HEIGHT,
                                 self.scroll_offset + 1)

    def handle_input(self, key):
        """处理滚动输入"""
        if key == pygame.K_PAGEUP:
            self.scroll_up()
            return True
        elif key == pygame.K_PAGEDOWN:
            self.scroll_down()
            return True
        return False

    def render(self, container):
        """Render messages with colored keywords"""
        msg_x, msg_y = 0, (HEADER_HEIGHT + MAP_HEIGHT) * self.char_height

        # Draw message log background
        msg_bg = pygame.Surface(
            (MSG_WIDTH * self.char_width, MSG_HEIGHT * self.char_height),
            pygame.SRCALPHA,
        )

        # Calculate visible messages
        start_idx = self.scroll_offset
        end_idx = min(start_idx + self.max_lines, len(self.messages))

        # Draw messages
        for i, (msg, color) in enumerate(self.messages[start_idx:end_idx]):
            render_colored_text(
                msg_bg,
                self.font,
                msg,
                (0, i * self.char_height),
                color,
            )

        container.blit(msg_bg, (msg_x, msg_y))
