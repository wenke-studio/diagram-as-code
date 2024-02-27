from __future__ import annotations

import os
from typing import Callable, Optional

from .base import Graph
from .properties import Properties
from .relations import ArrowType, Relations

__all__ = [
    "CloudArchitecture",
    "Node",
    "Group",
]


class CloudArchitecture(type):

    def __new__(mcs, name, bases, dct):
        """Create `._graphs` list to store all the graphs"""
        mcs._graphs = []
        return super().__new__(mcs, name, bases, dct)

    def __call__(cls, *args, **kwargs) -> Graph:
        """Initialize a graph object and add it to `._graphs`

        Retruns:
            Graph: The graph object
        """
        graph = super().__call__(*args, **kwargs)
        cls._graphs.append(graph)
        return graph

    @classmethod
    def draw(mcs, stdout: Callable | None = None) -> None:
        """Draw the diagram

        Args:
            stdout (Callable, optional): A function to handle the output. Defaults to None.
        """
        if stdout is None:
            stdout = print

        for graph in mcs._graphs:
            # sub-groups be rendered by the parent group
            if graph.parent is None:
                stdout(graph.render())

    @classmethod
    def reset(mcs) -> None:
        """Reset the `._graphs` list to an empty list

        useful for testing

        Args:
            mcs (CloudArchitecture): The metaclass
        """
        mcs._graphs = []


class Connection(Relations, Graph, metaclass=CloudArchitecture):
    """Connections represent relationships between nodes and groups.

    `Connection` inherit from Relations and register to the CloudArchitecture.

    Refs:
        https://docs.eraser.io/docs/syntax#connections
    """

    # This is used only in the `draw()` method of Cloud Architecture Diagrams
    parent = None


class Node(Graph, metaclass=CloudArchitecture):
    """Class to represent a node in the diagram"""

    def __init__(
        self, name: str, icon: Optional[str] = None, color: Optional[str] = None
    ) -> None:
        """Initialize the node

        Args:
            name (str): The name of the node
            icon (str, optional): The icon of the node. Defaults to None.
            color (str, optional): The color of the node. Defaults to None.
        """
        self.parent = None
        self.name = name
        self.properties = Properties(icon=icon, color=color)

    def connect(
        self, target: Graph, arrow: ArrowType = ArrowType.LEFT_TO_RIGHT_ARROW
    ) -> None:
        """Connect the node to another node or group"""
        Connection(source=self.name, target=target.name, relation=arrow)

    def render(self) -> str:
        """Render the node as a string

        Returns:
            str: The node as a string
        """
        return f"{self.name} {self.properties.render()}"


class Group(Graph, metaclass=CloudArchitecture):
    """Class to represent a group of nodes in the diagram"""

    def __init__(
        self, name: str, icon: Optional[str] = None, color: Optional[str] = None
    ) -> None:
        """Initialize the group

        Args:
            name (str): The name of the group
            icon (str, optional): The icon of the group. Defaults to None.
            color (str, optional): The color of the group. Defaults to None.
        """
        self.parent = None
        self.name = name
        self.properties = Properties(icon=icon, color=color)
        self.children: list[Graph] = []

    def connect(
        self, target: Graph, arrow: ArrowType = ArrowType.LEFT_TO_RIGHT_ARROW
    ) -> None:
        """Connect the node to another node or group"""
        Connection(source=self.name, target=target.name, relation=arrow)

    def append(self, *graphs: Graph) -> None:
        """Add nodes or groups to the group

        Args:
            *graphs (Graph): The nodes or groups to add
        """
        for graph in graphs:
            graph.parent = self
            self.children.append(graph)

    def render(self) -> str:
        """Render the group as a string

        Returns:
            str: The group as a string
        """
        header = f"{self.name} {self.properties.render()}"
        body = "\n".join((child.render() for child in self.children))
        return f"{header} {{{os.linesep}{body}{os.linesep}}}"
