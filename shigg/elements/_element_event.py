from abc import ABC, abstractmethod
from dataclasses import dataclass, is_dataclass, field, make_dataclass
from typing import ClassVar, Dict, Type
from enum import Enum, auto


class ElementEvent(ABC):
    def __init__(self, tag) -> None:
        # enforce tag to be an enum
        if not isinstance(tag, Enum):
            red = "\033[91m"
            endc = "\033[0m"
            raise TypeError(
                f"{red}The tag must be an Enum variant... not a {type(tag).__name__} (you passed in: {tag!r}). \
                \nThis is for your own good. What do you think this is, javascript?{endc}"
            )
        self.tag = tag

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value
