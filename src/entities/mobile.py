from entities.game_object import GameObject


class Mobile(GameObject):
    """可移动的实体，有位置信息且可以移动"""

    def __init__(self, mob_id: str, name: str, x: int, y: int, char: str, color: tuple, description: str = "", blocks: bool = True):
        super().__init__(mob_id, name, description)
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.blocks = blocks

    def move(self, dx: int, dy: int):
        """移动实体"""
        self.x += dx
        self.y += dy
