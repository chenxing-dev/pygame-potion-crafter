from entities.entity import Entity


class Actor(Entity):
    def __init__(self, e_id, x, y, char, color, name):
        super().__init__(e_id, x, y, char, color, name, blocks=True)

    def greet(self, target):
        """Greet another actor and return result message"""
        return f"{self.name} greets {target.name}!"
