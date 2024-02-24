from __future__ import annotations

from typing import Callable, Optional

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


class Graph:

    def render(self) -> str:
        pass


class Connection(Graph, metaclass=Sequence):
    def __init__(
        self, source: Node, message: str, target: Node, arrow: str = ">"
    ) -> None:
        self.source = source.name
        self.message = message
        self.target = target.name
        self.arrow = arrow

    def render(self) -> str:
        return f"{self.source} {self.arrow} {self.target} : {self.message}"


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


class Properties:
    """Class to represent the properties of a graph in the diagram"""

    def __init__(self, icon: Optional[str] = None, color: Optional[str] = None) -> None:
        """Initialize the icon and color of the graph

        Args:
            icon (str, optional): The icon of the graph. Defaults to None.
            color (str, optional): The color of the graph. Defaults to None.
        """
        self.icon = icon
        self.color = color

    def render(self) -> str:
        """Render the properties as a string

        Returns:
            str: The properties as a string
        """
        props = []
        if self.icon:
            props.append(f"icon: {self.icon}")
        if self.color:
            props.append(f"color: {self.color}")

        if props:
            return f"[{', '.join(props)}]"
        return ""


class Node(Graph, metaclass=Sequence):
    def __init__(
        self, name: str, icon: str | None = None, color: str | None = None
    ) -> None:
        self.name = name
        self.properties = Properties(icon, color)
        self.block = None

    def request(self, message: str, to: Node) -> None:
        Connection(self, message, to, arrow=">")

    def response(self, message: str, to: Node) -> None:
        Connection(self, message, to, arrow=">")

    def start_session(self, message: str, to: Node) -> None:
        Connection(self, message, to, arrow="<>")

    def do(self, message: str) -> None:
        Connection(self, message, self, arrow="-->")  # Dotted arrow

    def activate(self) -> None:
        Activation(self.name)

    def deactivate(self) -> None:
        Deactivate(self.name)

    def render(self) -> str:
        return f"{self.name} {self.properties.render()}"
