from abc import ABC


class Element(ABC):
    def __init__(self, tag) -> None:
        self.tag = tag
