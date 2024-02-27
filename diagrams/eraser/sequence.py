from __future__ import annotations

from typing import Callable

from .base import Graph
from .properties import Properties
from .relations import ArrowType, Relations

__all__ = [
    "Sequence",
    "Node",
    "Block",
]


class Sequence(type):
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
            output = graph.render()
            if output:
                stdout(output)

    @classmethod
    def reset(mcs):
        mcs._graphs = []


class Action(Relations, Graph, metaclass=Sequence):
    pass


class StartGroup(Graph, metaclass=Sequence):
    def __init__(self, name: str, label: str) -> None:
        self.name = name
        self.label = label

    def render(self) -> str:
        properties = ""
        if self.label:
            properties = f"[label: {self.label}]"
        return f"{self.name} {properties} {{"


class EndGroup(Graph, metaclass=Sequence):
    def render(self) -> str:
        return "}"


class Block:

    def __init__(self, name: str, label: str | None = None) -> None:
        StartGroup(name, label)

    def __enter__(self) -> None:
        pass

    def __exit__(self, *args, **kwargs) -> None:
        EndGroup()


class Activation(Graph, metaclass=Sequence):
    def __init__(self, name: str) -> None:
        self.name = name

    def render(self) -> str:
        return f"activate {self.name}"


class Deactivate(Graph, metaclass=Sequence):
    def __init__(self, name: str) -> None:
        self.name = name

    def render(self) -> str:
        return f"deactivate {self.name}"


class Node(Graph, metaclass=Sequence):
    def __init__(
        self, name: str, icon: str | None = None, color: str | None = None
    ) -> None:
        self.name = name
        self.properties = Properties(icon=icon, color=color)
        self.block = None

    def request(self, message: str, target: Node) -> None:
        """
        Request message from the source node to the target node

        request: `source > target`

        Args:
            message (str): Message to be displayed
            to (Node): Target node
        """
        Action(
            source=self.name,
            target=target.name,
            relation=ArrowType.LEFT_TO_RIGHT_ARROW,
            label=message,
        )

    def response(self, message: str, target: Node) -> None:
        """Response message from the target node to the source node

        response: `source > target`

        Args:
            message (str): Message to be displayed
            to (Node): Target node
        """
        Action(
            source=self.name,
            target=target.name,
            relation=ArrowType.LEFT_TO_RIGHT_ARROW,
            label=message,
        )

    def start_session(self, message: str, target: Node) -> None:
        """Start a session between the source node and the target node

        session: `source <> target`

        Args:
            message (str): Message to be displayed
            to (Node): Target node
        """
        Action(
            source=self.name,
            target=target.name,
            relation=ArrowType.BI_DIRECTIONAL_ARROW,
            label=message,
        )

    def do(self, message: str) -> None:
        """Do something itself

        Args:
            message (str): Message to be displayed
        """
        Action(
            source=self.name,
            target=self.name,
            relation=ArrowType.DOTTED_ARROW,
            label=message,
        )

    def activate(self) -> None:
        Activation(self.name)

    def deactivate(self) -> None:
        Deactivate(self.name)

    def render(self) -> str:
        return f"{self.name} {self.properties.render()}"
