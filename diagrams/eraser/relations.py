import enum

import attrs


class ArrowType(enum.Enum):
    DEFAULT = "-"

    LEFT_TO_RIGHT_ARROW = ">"
    RIGHT_TO_LEFT_ARROW = "<"
    BI_DIRECTIONAL_ARROW = "<>"
    LINE = "-"
    DOTTED_LINE = "--"
    DOTTED_ARROW = "-->"


class EntityRelationshipType(enum.Enum):
    DEFAULT = "-"

    ONE_TO_ONE = "-"
    ONE_TO_MANY = "<"
    MANY_TO_ONE = ">"
    MANY_TO_MANY = "<>"


@attrs.define(kw_only=True)
class Relations:
    source: str
    target: str
    relation: ArrowType | EntityRelationshipType = ArrowType.DEFAULT
    label: str | None = None

    def render(self) -> str:
        """Render the relationship between the source and target"""
        if self.label is None:
            return f"{self.source} {self.relation.value} {self.target}"
        return f"{self.source} {self.relation.value} {self.target} : {self.label}"
