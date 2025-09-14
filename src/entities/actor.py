from entities.entity import Entity


class Actor(Entity):
    def __init__(self, x, y, char, color, name):
        super().__init__(x, y, char, color, name, blocks=True)
        self.alive = True

    def greet(self, target):
        """Greet another actor and return result message"""
        return f"{self.name} greets {target.name}!"
