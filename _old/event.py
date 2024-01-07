from dataclasses import dataclass, is_dataclass, field, make_dataclass
from typing import ClassVar, Dict, Type


class DataEventMeta(type):
    def __new__(mcs, name, bases, attrs):
        # Create the class normally first
        cls = super().__new__(mcs, name, bases, attrs)

        # If this is not the base Event class
        if name != "Event":
            # Add default fields for all annotated attributes
            annotations = attrs.get("__annotations__", {})
            for attr_name, attr_type in annotations.items():
                if attr_name not in attrs:
                    attrs[attr_name] = field(default=None)

            # Convert the subclass into a data class
            cls = dataclass(cls)

            # Register the subclass in the shared registry
            bases[0].register(cls)  # Assumes Event is the first base class

        return cls


class Event(metaclass=DataEventMeta):
    """Event base that can optionally hold data."""

    _registry: ClassVar[Dict[str, Type["Event"]]] = dict()

    @classmethod
    def register(cls, event_cls):
        cls._registry[event_cls.__name__] = event_cls

    @classmethod
    def all(cls):
        return list(cls._registry.values())

    def __eq__(self, other):
        """Events are equal if they are of the same type, despite having different inner data.
        (Inteded to be like an enum)"""
        return type(self) == type(other)

    def __ne__(self, other):
        """Only considers the event type, not the inner data."""
        return not self.__eq__(other)

    def __repr__(self):
        """Default repr which displays all instance members.
        Ignores named args that are default None"""
        attrs = ", ".join(
            f"{k}={v!r}" for k, v in self.__dict__.items() if v is not None
        )
        return f"{self.__class__.__name__}({attrs})"
