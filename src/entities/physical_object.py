from entities.game_object import GameObject, ObjectType


class PhysicalObject(GameObject):
    """A physical object in the game world."""

    def __init__(
        self,
        obj_id: str,
        object_type: ObjectType,
        blocks: bool = True,
        interactable: bool = False
    ):
        super().__init__(obj_id, object_type)
        self.blocks = blocks
        self.interactable = interactable
