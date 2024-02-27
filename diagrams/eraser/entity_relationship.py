from __future__ import annotations

import os
from typing import Callable

from .properties import Properties

__all__ = [
    "EntityRelationship",
    "Entity",
]


class EntityRelationship(type):
    def __new__(mcs, name, bases, dct):
        mcs._graphs = []
        return super().__new__(mcs, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        graph = super().__call__(*args, **kwargs)
        cls._graphs.append(graph)
        return graph

    @classmethod
    def draw(mcs, stdout: Callable = None):
        if stdout is None:
            stdout = print
        for graph in mcs._graphs:
            stdout(graph.render())
        for graph in mcs._graphs:
            for attribute in graph.attributes:
                output = attribute.edges.render()
                if output:
                    stdout(output)

    @classmethod
    def reset(mcs):
        mcs._graphs = []


class Graph:

    def render(self) -> str:
        raise NotImplementedError("`.render()` method should be implemented")


class Edge(Graph):
    def __init__(self, source: str) -> None:
        """Initialize the source and targets of the edge

        Args:
            source (Attribute): The source attribute
        """
        self.source: str = source
        self.targets: list[tuple[str, str]] = []

    def one_to_many(self, target: str) -> None:
        self.targets.append(("<", f"{target.parent_name}.{target.name}"))

    def many_to_one(self, target: str) -> None:
        self.targets.append((">", f"{target.parent_name}.{target.name}"))

    def one_to_one(self, target: str) -> None:
        self.targets.append(("-", f"{target.parent_name}.{target.name}"))

    def many_to_many(self, target: str) -> None:
        self.targets.append(("<>", f"{target.parent_name}.{target.name}"))

    def render(self) -> str:
        return "\n".join(
            (f"{self.source} {relation} {target}" for relation, target in self.targets)
        )


class Attribute(Graph):
    def __init__(
        self, parent_name: str, name: str, data_type: str = "", metadata: str = ""
    ) -> None:
        self.parent_name = parent_name
        self.name = name
        self.data_type = data_type
        self.metadata = metadata
        self.edges = Edge(f"{self.parent_name}.{self.name}")

    def render(self) -> str:
        return f"{self.name} {self.data_type} {self.metadata}".strip()


class Entity(Graph, metaclass=EntityRelationship):
    def __init__(
        self, name: str, icon: str | None = None, color: str | None = None
    ) -> None:
        self.name = name
        self.properties = Properties(icon=icon, color=color)
        self.attributes = []

    def add_attribute(self, name: str, data_type: str = "", metadata: str = "") -> None:
        attribute = Attribute(self.name, name, data_type, metadata)
        self.attributes.append(attribute)
        return attribute

    def render(self) -> str:
        header = f"{self.name} {self.properties.render()}"
        body = "\n".join(attribute.render() for attribute in self.attributes)
        return f"{header} {{{os.linesep}{body}{os.linesep}}}"
