from __future__ import annotations

import os
from typing import Callable, Optional

from .properties import Properties

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

        # nodes and groups
        for graph in mcs._graphs:
            if graph.parent is None:
                stdout(graph.render())
        # connections
        for graph in mcs._graphs:
            output = graph.edges.render()
            if output:
                stdout(output)

    @classmethod
    def reset(mcs) -> None:
        """Reset the `._graphs` list to an empty list

        useful for testing

        Args:
            mcs (CloudArchitecture): The metaclass
        """
        mcs._graphs = []


class Graph:
    """Base class for all graphs in the diagram"""

    name: str

    def render(self) -> str:
        """Render the graph as a string"""

    @property
    def parent(self) -> Graph:
        """Get the parent graph"""
        return self._parent

    @parent.setter
    def parent(self, graph: Graph) -> None:
        """Set the parent graph"""
        self._parent = graph


class Edge:
    """Class to represent the connections between graphs in the diagram"""

    def __init__(self, source: Graph) -> None:
        """Initialize the source and targets of the edge

        Args:
            source (Graph): The source graph
        """
        self.source: str = source.name
        self.targets: list[str] = []

    def connect(self, *graphs: Graph) -> None:
        """Connect the source graph to the target graphs

        Args:
            *graphs (Graph): The target graphs
        """
        for graph in graphs:
            self.targets.append(graph.name)

    def render(self) -> str:
        """Render the edge as a string

        Left-to-right arrow

        Returns:
            str: The edge as a string
        """
        if self.targets:
            return f"{self.source} > {', '.join(self.targets)}"
        return ""


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
        self.edges = Edge(self)

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
        self.edges = Edge(self)
        self.children: list[Graph] = []

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
