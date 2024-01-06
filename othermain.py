from dataclasses import dataclass, is_dataclass
from typing import ClassVar, Dict, Type


class DataEventMeta(type):
    def __new__(mcs, name, bases, attrs):
        if bases and not is_dataclass(bases[0]):
            cls = dataclass(super().__new__(mcs, name, bases, attrs))
        else:
            cls = super().__new__(mcs, name, bases, attrs)

        if bases:  # Prevents registration of the base Event class itself
            cls.register(cls)
        return cls


@dataclass
class Event(metaclass=DataEventMeta):
    """Event base that can optionally hold data."""

    _registry: ClassVar[Dict[str, Type["Event"]]] = dict()  # Direct assignment

    @classmethod
    def register(cls, event_cls):
        """Register a new event type. You should not call this."""
        cls._registry[event_cls.__name__] = event_cls

    @classmethod
    def all(cls):
        """Return all registered events."""
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


class SimpleNotification(Event):
    pass


class Numpad(Event):
    def __init__(self, number):
        super().__init__()
        self.number = number


class Message(Event):
    def __init__(self, content=None):
        super().__init__()
        self.message = content


class Message2(Event):
    content: str = None


# Usage
event1 = Numpad(1)
event2 = Numpad(2)
event3 = SimpleNotification()

print(Event.all())  # All registered events
print(event1 == event2)  # True, as they are both NumpadEvent types
print(event1 == event3)  # False, different event types
print(event1)  # NumpadEvent(number=5)

event4 = Message()
event5 = Message("Hello World!")
print(event4)  # Message()
print(event5)  # Message(message='Hello World!')
