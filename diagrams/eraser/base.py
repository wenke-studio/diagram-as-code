from __future__ import annotations


class Graph:
    """Base class for all graphs in the diagram"""

    @property
    def name(self) -> str:
        """Graph name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the graph name"""
        self._name = value

    @property
    def parent(self) -> Graph:
        """Graph parent"""
        return self._parent

    @parent.setter
    def parent(self, graph: Graph) -> None:
        """Set the graph parent"""
        self._parent = graph

    def render(self) -> str:
        """Render the graph as a string"""
        raise NotImplementedError("`.render()` should be implemented")
