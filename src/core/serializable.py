"""A mixin class for serializable objects."""
from typing import Any, Dict


class Serializable:
    """A mixin class for serializable objects."""

    def __init__(self):
        self._serializable_exclude = set()  # Attributes to exclude from serialization

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary of the object's state that should be saved."""
        # Default implementation: save all instance variables that are not callable and do not start with '_'
        print(
            f"serializable: Serializing object: {self.__class__.__name__} with id: {getattr(self, 'id', 'N/A')}")
        data = {}
        for key, value in self.__dict__.items():
            if key not in self._serializable_exclude:
                if not callable(value) and not key.startswith('_'):
                    if hasattr(value, 'to_dict'):
                        # 如果属性本身是可序列化的对象，递归调用to_dict
                        data[key] = value.to_dict()
                    else:
                        data[key] = value
        return data

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Takes a dictionary of saved state and returns an instance of the class.
        Override this in subclasses for more complex deserialization logic.
        """
        for key, value in data.items():
            if hasattr(self, key):
                current_attr = getattr(self, key)
                # If the current attribute is serializable, we might want to call its from_dict method
                if hasattr(current_attr, 'from_dict') and isinstance(value, dict):
                    current_attr.from_dict(value)
                else:
                    setattr(self, key, value)
