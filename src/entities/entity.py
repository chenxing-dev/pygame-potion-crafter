class Entity:
    def __init__(self, e_id: str, x: int, y: int, char: str, color: str, name: str, blocks=False):
        self.id = e_id
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
